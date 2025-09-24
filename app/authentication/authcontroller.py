from fastapi import HTTPException,status
from passlib.context import CryptContext
import jwt
from app.authentication.dtos import UserSchema,LoginSchema

from sqlalchemy.orm import Session
from app.e_commerce.models import User,Category,CartItem,Order
from datetime import datetime,timedelta,timezone
from app.utlis.helper import is_admin

# ------------user-----------------


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hassed(password):
    return pwd_context.hash(password)

# ---------register/create user-----------

def register_user(body:UserSchema,db:Session):
    existing_user=db.query(User).filter(User.username==body.username).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user already exist for this username ")
    
    hp=get_password_hassed(body.password)

    newUser=User(
        name=body.name,
        username=body.username,
        email=body.email,
        mobile=body.mobile,
        hass_password=hp,
        is_superuser=body.is_superuser,
        is_active=body.is_active,
        is_seller=body.is_seller
    )

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return {"status":"ok","user":newUser}

# ---------------------login user--------------------


SECRET_KEY="TYUIK345678DSVBN56789ODHSFGHJK890OJN"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def verify_password(plain_password,hasshed_password):
    return pwd_context.verify(plain_password,hasshed_password)

def get_user_by_username(username:str,db:Session):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    
    return user

def login_user(body:LoginSchema,db:Session):
    current_user=get_user_by_username(body.username,db)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found for this username")
    
    varify_pass=verify_password(body.password,current_user.hass_password)
    if not varify_pass:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="password not found")
    
    expire= datetime.now(timezone.utc)+timedelta(minutes=30)
    token=jwt.encode({"username":current_user.username,"exp":expire},SECRET_KEY,algorithm=ALGORITHM)
    return {"token":token,"message":"you loggedin successfully"}

# ---------------------update user--------------------------

def update_user(body:UserSchema,user:User,db:Session):
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    
    if is_admin(user):  # if the user is superuser he can access everything.

        user.name=body.name
        user.email=body.email
        user.username=body.username
        user.mobile=body.mobile
        user.hass_password=pwd_context.hash(body.password)
        user.is_seller=body.is_seller
        user.is_active=body.is_active
        user.is_superuser=body.is_superuser

        db.commit()
        db.refresh(user)
        return{"status":"ok","user":user}
    
    elif user.is_seller :  # if the user is only seller he cannot access superuser and seller properties.

        user.name=body.name
        user.email=body.email
        user.username=body.username
        user.mobile=body.mobile
        user.hass_password=pwd_context.hash(body.password)
        user.is_active=body.is_active

        db.commit()
        db.refresh(user)
        return{"status":"ok","user":user}
    
    elif user.is_active:   # if the user is only normal user he cannot access superuser and seller and active properties.

        user.name=body.name
        user.email=body.email
        user.username=body.username
        user.mobile=body.mobile
        user.hass_password=pwd_context.hash(body.password)

        db.commit()
        db.refresh(user)
        return{"status":"ok","user":user}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user"
        )
    
# ---------------------delete user-------------------

def delete_user(user:User,db:Session,user_id:int=None):
    if is_admin(user):     # if the user is superuser he can delete anyones account.
        if not user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user_id is required")
        current_user=db.query(User).filter(User.id==user_id).first()
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        db.delete(current_user)
        db.commit()
        return{"status":"ok","message":"user deleted succesfully"}
    
    else:  # if the user is normal user or seller they can delete only there account.
        current_user=db.query(User).filter(User.id==user.id).first()
        if not current_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        db.delete(current_user)
        db.commit()
        return{"status":"ok","message":"user deleted succesfully"}
    
        
    





# -------------------User profile seller/normalUser------------------

def get_user_profile(user:User,db:Session):

    if is_admin(user):   # If the user is a superuser/admin, return only their information.
         return{
              "user":{
                    "id":user.id,
                    "name":user.name,
                    "username":user.username,
                    "mobile":user.mobile,
                    "email":user.email,
                    "is_seller":user.is_seller,
                    "is_active":user.is_active,
                    "is_superuser":user.is_superuser
                    }
         }
    
    elif user.is_seller:    # If the user is a seller, fetch the categories assigned to them.
     
         category=db.query(Category).filter(Category.user_id==user.id).all()

    
         return{
               "user":{
                    "id":user.id,
                    "name":user.name,
                    "username":user.username,
                    "mobile":user.mobile,
                    "email":user.email,
                    "is_seller":user.is_seller,
                    "is_active":user.is_active

                },"category":category
        }
    
    
    elif user.is_active and not user.is_seller :   # If the user is active but not a seller, fetch their cart and order items.
    
         cart_Item=db.query(CartItem).filter(CartItem.user_id==user.id).all()
         ordered_Item=db.query(Order).filter(Order.user_id==user.id).all()

    
         return{
              "user":{
                  "id":user.id,
                  "name":user.name,
                  "username":user.username,
                  "mobile":user.mobile,
                  "email":user.email,
                  "is_active":user.is_active
            },
            "cart_Item":cart_Item,
            "ordered_Item":ordered_Item

        }
    
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you are unauthorized")
    

