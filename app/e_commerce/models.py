from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from app.utlis.db import Base


class User(Base):
        __tablename__="user"

        id=Column(Integer,primary_key=True)
        name=Column(String,nullable=False)
        email=Column(String,nullable=False)
        mobile=Column(Integer,unique=True)
        username=Column(String,unique=True,nullable=False)
        hass_password=Column(String)
        is_superuser=Column(Boolean,default=False)
        is_active=Column(Boolean,default=True)
        is_seller=Column(Boolean,default=False)

class Category(Base):
        __tablename__="category"

        id=Column(Integer,primary_key=True)
        name=Column(String,unique=True)
        user_id=Column(Integer,ForeignKey("user.id"),nullable=False)

class Product(Base):
        __tablename__="product"

        id=Column(Integer,primary_key=True)
        name=Column(String,nullable=False,unique=True)
        description=Column(String,nullable=False)
        price=Column(Integer,nullable=False)
        
        image=Column(String)
        in_stock=Column(Integer,default=0)
        cat_id=Column(Integer,ForeignKey("category.id"),nullable=False)
        user_id=Column(Integer,ForeignKey("user.id"),nullable=False)

class CartItem(Base):
        __tablename__="cart_item"

        id=Column(Integer,primary_key=True)
        count=Column(Integer,default=0)
        pro_id=Column(Integer,ForeignKey("product.id"),nullable=False)
        user_id=Column(Integer,ForeignKey("user.id"),nullable=False)
        pro_name=Column(String,ForeignKey("product.name"),nullable=False)
        pro_pirce=Column(String,ForeignKey("product.price"),nullable=False)

class Addresses(Base):
        __tablename__="addresses"

        id=Column(Integer,primary_key=True)
        user_id=Column(Integer,ForeignKey("user.id"),nullable=False)
        city=Column(String,nullable=False)
        state=Column(String,nullable=False)
        pincode=Column(Integer,nullable=False)
        fullAddress=Column(String,nullable=False)

class Order(Base):
        __tablename__="orders"

        id=Column(Integer,primary_key=True)
        user_id=Column(Integer,ForeignKey("user.id"),nullable=False)
        total_price=Column(Integer,nullable=False)
        status=Column(String,default="Placed")
        address_id=Column(Integer,ForeignKey("addresses.id"),nullable=False)
        cart_id=Column(Integer,ForeignKey("cart_item.id"),nullable=False)

