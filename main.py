from fastapi import FastAPI
from app.utlis.db import db_init,Base
from app.authentication.router import api_auth
from app.e_commerce.router import api


app=FastAPI()
app.include_router(api)
app.include_router(api_auth)

Base.metadata.create_all(bind=db_init)

@app.get("/test")
def home():
    return {"message":"welcome to Todolist"}
