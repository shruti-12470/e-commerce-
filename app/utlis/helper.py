from fastapi import Request,HTTPException,status,Depends
import jwt
# from app.authentication.authcontroller import get_user_by_username
from sqlalchemy.orm import Session
from app.utlis.db import get_db
from app.e_commerce.models import User

SECRET_KEY="TYUIK345678DSVBN56789ODHSFGHJK890OJN"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def get_user_by_username(username:str,db:Session):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    
    return user


def is_authenticated(req:Request,db:Session=Depends(get_db)):
    print("All headers:", req.headers)
    token=req.headers.get("authorization")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not authorized")
    
    token=token.split(" ")[-1]
    data =jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
    print("Decoded JWT payload:", data)

    if not data.get("username"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not authorized")
    
    user=get_user_by_username(data.get("username"),db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are not authorized")
    return user


def is_admin(user:User) :
    return user.is_superuser