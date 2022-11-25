from fastapi import FastAPI
from src.routers.rest_router import rest_router
from src.routers.grpc_router import grpc_router
from src.routers.auth_router import auth_router
from fastapi.middleware.cors import CORSMiddleware


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

app.include_router(auth_router)
app.include_router(rest_router)
app.include_router(grpc_router)
