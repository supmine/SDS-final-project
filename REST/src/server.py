import bson
from fastapi import FastAPI, APIRouter, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.schema import CreateUserSchema, LoginUserSchema, DatasetSchema, AnnotateSchema
from src.utils import get_password_hash, verify_password, create_access_token
from src.database import (
    find_user_by_email,
    find_user_by_id,
    add_user,
    add_dataset,
    get_all_datasets,
    find_dataset_by_id,
    set_user_balance,
    replace_dataset_by_id,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


user_router = APIRouter(
    prefix="/auth", tags=["user"], responses={404: {"descrption": "Not Found"}}
)


@user_router.post("/create")
async def create_user(request: CreateUserSchema):
    request = request.__dict__
    email = request["email"]
    password = request["password"]
    request["password"] = get_password_hash(password)
    request["balance"] = 0
    user = await find_user_by_email(email)
    if user:
        raise HTTPException(status_code=409, detail="Email Already Found")
    inserted_user = await add_user(request)
    print(inserted_user)
    return {"ok": 1}


@user_router.post("/login")
async def login_user(request: LoginUserSchema):
    request = request.__dict__
    email = request["email"]
    plain_password = request["password"]
    user = await find_user_by_email(email)
    if user:
        hashed_password = user["password"]
        if verify_password(plain_password, hashed_password):
            return {
                "token": create_access_token(
                    {"email": user["email"], "user_id": user["user_id"]}
                ),
                "token_type": "BEARER",
            }
    raise HTTPException(status_code=400, detail="User or Password incorrect")


dataset_router = APIRouter(
    prefix="/dataset", tags=["dataset"], responses={404: {"descrption": "Not Found"}}
)


@dataset_router.get("/")
async def dump_dataset_collection():
    datasets = await get_all_datasets()
    print(datasets)
    return datasets


@dataset_router.get("/{id}")
async def get_a_dataset(id: str):
    dataset = await find_dataset_by_id(id)
    return dataset


@dataset_router.post("/create")
async def create_dataset(request: DatasetSchema):
    request = request.__dict__
    request["entries"] = [e.__dict__ for e in request["entries"]]
    reward_per_entry = round(request["reward_dataset"] / len(request["entries"]), 2)
    for idx, entry in enumerate(request["entries"]):
        temp = entry
        temp["entry_id"] = bson.ObjectId()
        temp["reward"] = reward_per_entry
        request["entries"][idx] = temp
    dataset = await add_dataset(request)
    dataset = await find_dataset_by_id(dataset)
    return dataset


annotate_router = APIRouter(
    prefix="/annotate", tags=["annotate"], responses={404: {"descrption": "Not Found"}}
)


@annotate_router.put("/")
async def annotate(request: AnnotateSchema):
    request = request.__dict__
    dataset = await find_dataset_by_id(request["dataset_id"])
    user = await find_user_by_id(str(request["labeler_id"]))
    for entry in dataset["entries"]:
        if entry["entry_id"] == request["entry_id"]:
            entry["label"] = request["label"]
            entry["labeler_id"] = request["labeler_id"]
            break
    await replace_dataset_by_id(request["dataset_id"], dataset)
    await set_user_balance(request["labeler_id"], user["balance"] + entry["reward"])
    return entry


app.include_router(user_router)
app.include_router(dataset_router)
app.include_router(annotate_router)
