from fastapi import APIRouter,Depends
from app.authentication.dtos import UserSchema,LoginSchema
from app.authentication.authcontroller import register_user,login_user,update_user,delete_user,get_user_profile
from app.utlis.helper import is_authenticated
from app.e_commerce.models import User
from sqlalchemy.orm import Session
from app.utlis.db import get_db

api_auth=APIRouter(prefix="/auth")

# ---------register/create user-----------

@api_auth.post("/register")
def createUser(body:UserSchema,db:Session=Depends(get_db)):
    return register_user(body,db)

# ---------------------login user--------------------

@api_auth.get("/login")
def loginUser(body:LoginSchema,db:Session=Depends(get_db)):
    return login_user(body,db)

# ---------------------update user--------------------------

@api_auth.put("/updateUser")
def updateUser(body:UserSchema,user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return update_user(body,user,db)

# ---------------------delete user-------------------

@api_auth.delete("/deleteUser")
def deleteUser(user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return delete_user(user,db)

# -------------------User profile seller/normalUser------------------

@api_auth.get("/userProfile")
def userProfile(user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return get_user_profile(user,db)