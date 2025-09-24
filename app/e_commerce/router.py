from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.utlis.db import get_db
from app.utlis.helper import is_authenticated
from app.e_commerce.dtos import ProductSchema,CategorySchema,AddressSchema,CartItemSchema,OrderSchema
from app.e_commerce.models import User
from app.e_commerce.controller import create_category,get_category,update_category,delete_category
from app.e_commerce.controller import create_product,get_product,update_product,delete_product
from app.e_commerce.controller import create_address,get_address,update_address,delete_address
from app.e_commerce.controller import create_cartItem,get_cartItem,update_cartItem,delete_cartItem
from app.e_commerce.controller import create_order,get_orders,update_order,delete_order

api=APIRouter(prefix="/e_commerce")


# ---------------------CREATE CATEGORY-----------

@api.post("/category")
def createCategory(body:CategorySchema,user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return create_category(body,user,db)

# ---------------------GET CATEGORY--------------------

@api.get("/category")
def getCategory(user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return get_category(user,db)

# ---------------------UPDATE CATEGORY--------------------------

@api.put("/category")
def updateCategory(cat_id:int,body:CategorySchema,user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return update_category(cat_id,body,user,db)

# ---------------------DELETE CATEGORY-------------------

@api.delete("/category")
def deleteCategory(cat_id:int,user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return delete_category(cat_id,user,db)




# ---------------------CREATE PRODUCT--------------

@api.post("/product")
def createProduct(body:ProductSchema,user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return create_product(body,user,db)

# ---------------------GET PRODUCT--------------------

@api.get("/product")
def getProduct(user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return get_product(user,db)

# ---------------------UPDATE PRODUCT--------------------------

@api.put("/product")
def updateProduct(pro_id:int,body:ProductSchema,user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return update_product(pro_id,body,user,db)

# ---------------------DELETE PRODUCT-------------------

@api.delete("/product")
def deleteProduct(pro_id:int,user:User=Depends(is_authenticated),db:Session=Depends(get_db)):
    return delete_product(pro_id,user,db)


# ---------------------CREATE ADDRESS---------------------

@api.post("/address")
def createAddress(body: AddressSchema,user: User = Depends(is_authenticated),db: Session = Depends(get_db)):
    return create_address(body, db, user)

# ---------------------GET ADDRESS---------------------

@api.get("/address")
def getAddress(user: User = Depends(is_authenticated),db: Session = Depends(get_db)):
    return get_address(db, user)

# ---------------------UPDATE ADDRESS--------------------

@api.put("/address")
def updateAddress(addre_id: int,body:AddressSchema, db: Session = Depends(get_db),user: User = Depends(is_authenticated)):
    return update_address(addre_id, body, db, user)

# ---------------------DELETE ADDRESS---------------------

@api.delete("/address")
def deleteAddress(addre_id: int, db: Session = Depends(get_db), user: User = Depends(is_authenticated)):
    return delete_address(addre_id, db, user)

# ---------------------CREATE CARTITEM-------------------------

@api.post("/cartItem")
def createCartItem( body: CartItemSchema,db: Session = Depends(get_db),user: User = Depends(is_authenticated)):
    return create_cartItem(body, user, db)


# ---------------------GET CARTITEM----------------------------

@api.get("/cartItem")
def getCartItems(db: Session = Depends(get_db),user: User = Depends(is_authenticated)):
    return get_cartItem(user, db) 


# ---------------------UPDATE CARTITEM----------------------------

@api.put("/cartItem")
def updateCartItem(pro_id: int,body: CartItemSchema,db: Session = Depends(get_db),user: User = Depends(is_authenticated)):
    return update_cartItem(pro_id,body,user,db)



# ---------------------DELETE CARTITEM----------------------------


@api.delete("/cartItem")
def deleteCartItem(cart_id: int, db: Session = Depends(get_db),user: User = Depends(is_authenticated)):
    return delete_cartItem(cart_id, user, db)



# ---------------------CREATE ORDER-------------------------

@api.post("/order")
def createOrder( body: CartItemSchema,db: Session = Depends(get_db),user: User = Depends(is_authenticated)):
    return create_order(body, user, db)


# ---------------------GET ORDER----------------------------

@api.get("/order")
def getOrders(db: Session = Depends(get_db),user: User = Depends(is_authenticated), user_id :int= None):
    return get_orders(db,user,user_id) 


# ---------------------UPDATE ORDER----------------------------

@api.put("/order")
def updateOrder(body:OrderSchema,db: Session=Depends(get_db), user:User=Depends(is_authenticated),order_id:int= None, user_id :int= None):
    return update_order(body,user,db,order_id,user_id)

# ---------------------DELETE ORDER----------------------------

@api.delete("/order")
def deleteOrder(db: Session=Depends(get_db), user:User=Depends(is_authenticated),order_id:int= None, user_id :int= None):
    return delete_order(user, db,user_id,order_id)