from pydantic import BaseModel
from typing import Literal

class CategorySchema(BaseModel):
        name:str  
        
class ProductSchema(BaseModel):
        name:str 
        description:str
        price:int
        availability:int
        image:str
        in_stock:int
        cat_id:int

class CartItemSchema(BaseModel):
        count:int
        pro_id:int



class AddressSchema(BaseModel):
        city:str
        state:str
        pincode:str
        fullAddress:str

class OrderSchema(BaseModel):
        pro_id:int
        count:int
        total_price:int
        status:Literal["order placed","order pending","order cancel"]
        address:str

