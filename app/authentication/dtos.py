from pydantic import BaseModel

class UserSchema(BaseModel):
        name:str
        email:str
        mobile:int
        username:str
        password:str
        is_superuser:bool=False
        is_active:bool=True
        is_seller:bool=False


class LoginSchema(BaseModel):
        username:str  
        password:str
        











