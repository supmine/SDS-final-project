from fastapi import APIRouter, Depends, HTTPException
from src.database import find_user_by_email, add_user
from src.schema import CreateUserSchema, LoginUserSchema
from src.utils import get_password_hash, verify_password, create_access_token, validate_token

auth_router = APIRouter(
    prefix="/auth", tags=["auth"], responses={404: {"description": "Not Found"}}
)

@auth_router.post("/register")
async def create_account(request: CreateUserSchema):
    request = request.__dict__
    email = request["email"]
    password = request["password"]
    request["password"] = get_password_hash(password)
    request["balance"] = 0
    user = await find_user_by_email(email)
    if user:
        raise HTTPException(status_code=409, detail="Email Already Found")
    inserted_user = await add_user(request)
    return {"ok": 1}

@auth_router.post("/login")
async def login(request: LoginUserSchema):
    request = request.__dict__
    user = await find_user_by_email(request["email"])
    if not user or not verify_password(request["password"], user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    jwt = create_access_token({"email": user["email"], "user_id": user["user_id"]})
    return {"token": jwt, "token_type": "BEARER"}

@auth_router.get("/user")
async def get_current_user(user=Depends(validate_token)):
    return user