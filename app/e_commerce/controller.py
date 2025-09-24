from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from app.e_commerce.models import *
from app.e_commerce.dtos import *
from app.utlis.helper import is_admin


# ---------------------CATEGORY------------------


# -------------------CREATE CATEGORY------------------------
def create_category(body:CategorySchema,user:User,db:Session):
    if not is_admin(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you are not authorized")
    
    existing_category = db.query(Category).filter(Category.name == body.name).first()
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists"
        )
    
    newCategory=Category(
         name=body.name,
         user_id=user.id
        )

    db.add(newCategory)
    db.commit()
    db.refresh(newCategory)

    return{"status":"created successfully","newcategory":newCategory}

# -------------------GET CATEGORY------------------------
def get_category(user:User,db:Session):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you are not authorized")

    categories=db.query(Category).all()
    return{"categories":categories}
    
# ----------------UPDATE CATEGORY------------------------

def update_category(cat_id:int,body:CategorySchema,user:User,db:Session):
    if not is_admin(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you are not authorized")
    

    category=db.query(Category).filter(Category.id==cat_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    category.name=body.name
    category.user_id=user.id

    db.commit()
    db.refresh(category)
    return{"status":"updated successfully","category":category}

# -------------------DELETE CATEGORY------------------------
def delete_category(cat_id:int,user:User,db:Session):
    if not is_admin(user):
        raise HTTPException (status_code=status.HTTP_400_BAD_REQUEST,detail="you are not authorized")
    
    
    category=db.query(Category).filter(Category.id==cat_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    db.delete(category)
    db.commit()
    return{"status":"ok","message":"category deleted successfully"}
    



# ----------------------PRODUCT---------------------------
# ---------------------CREATE PRODUCT---------------------

def create_product(body:ProductSchema,user:User,db:Session):
    if not is_admin(user) and not user.is_seller:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="only sellers and admins can add product")
    
    existing_product = db.query(Product).filter(Product.name == body.name).first()
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product with this name already exists"
        )

    newproduct=Product(
            name=body.name,
            description=body.description,
            price=body.price,
            availability=body.availability,
            image=body.image,
            in_stock=body.in_stock,
            cat_id=body.cat_id,
            user_id=user.id

       )

    db.add(newproduct)
    db.commit()
    db.refresh(newproduct)
    return {"status": "created", "product": newproduct}


# -------------------GET PRODUCT------------------------
def get_product(user:User,db:Session):
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you are not authorized")

    product=db.query(Product).all()
    return{"products":product}



# ----------------UPDATE PRODUCT------------------------

def update_product(pro_id:int,body:ProductSchema,user:User,db:Session):
    product = db.query(Product).filter(Product.id == pro_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if is_admin(user):
        product.name=body.name
        product.description=body.description
        product.price=body.price
        product.availability=body.availability
        product.image=body.image
        product.in_stock=body.in_stock
        product.cat_id=body.cat_id

        db.commit()
        db.refresh(product)
        return{"status":"updated successfully","product":product}

    if (user.is_seller and product.user_id == user.id):
        product.name=body.name
        product.description=body.description
        product.price=body.price
        product.availability=body.availability
        product.image=body.image
        product.in_stock=body.in_stock
        product.cat_id=body.cat_id
        product.user_id=user.id

        db.commit()
        db.refresh(product)
        return{"status":"updated successfully","product":product}
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not allowed to update this product")


# -------------------DELETE PRODUCT------------------------

def delete_product(pro_id:int,user:User,db:Session):
    product = db.query(Product).filter(Product.id == pro_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Product not found")

    if is_admin(user):
       db.delete(product)
       db.commit()

       return{"status":"ok","message":"product deleted successfully"} 
    
    elif user.is_seller and product.user_id==user.id:
        db.delete(product)
        db.commit()

        return{"status":"ok","message":"product deleted successfully"}
    
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not allowed to delete this product"
        )

# ----------------------ADDRESS---------------------------
# ---------------------CREATE ADDRESS---------------------
  
    
def create_address(body:AddressSchema , db:Session , user:User):
    existing_address=db.query(Addresses).filter(Addresses.user_id==user.id,Addresses.fullAddress==body.fullAddress).first()
    if existing_address:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="address already exists"
        )
    if is_admin(user):
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="admins cannot add address"
        )


    NewAddress = Addresses(user_id = user.id,
                        city = body.city,
                        state = body.state,
                        pincode = body.pincode,
                        fullAddress = body.fullAddress
                        )
    db.add(NewAddress)
    db.commit()
    db.refresh(NewAddress)
    return {"status":"ok","message":"address is successfully added","address":NewAddress}
    
       

# ---------------------GET ADDRESS---------------------

def get_address(db:Session , user:User):
    if is_admin(user):
        addressess=db.query(Addresses).all()
        return {"addressess":addressess}
    
    address=db.query(Addresses).filter(Addresses.user_id==user.id).all()
    if not address:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Address not found")
    return {"address":address}
    
    

# ---------------------UPDATE ADDRESS---------------------

def update_address(addre_id:int, body:AddressSchema , db:Session , user:User):
    if is_admin(user):

        Updateaddress = db.query(Addresses).filter(Addresses.id == addre_id).first()
        if not Updateaddress:
            raise HTTPException(status_code=404 , detail="Address not found")
        Updateaddress.city = body.city
        Updateaddress.state = body.state
        Updateaddress.pincode = body.pincode
        Updateaddress.fullAddress = body.fullAddress

        db.commit()
        db.refresh(Updateaddress)
        return {"status":"ok","message":"adress updated successfully","address":Updateaddress}

    else:

        Updateaddress=db.query(Addresses).filter(Addresses.user_id==user.id,Addresses.id==addre_id).first()
        if not Updateaddress:
            raise HTTPException(status_code=404 , detail="Address not found")
        Updateaddress.city = body.city
        Updateaddress.state = body.state
        Updateaddress.pincode = body.pincode
        Updateaddress.fullAddress = body.fullAddress

        db.commit()
        db.refresh(Updateaddress)
        return {"status":"ok","message":"adress updated successfully","address":Updateaddress}



# ---------------------DELETE ADDRESS---------------------

def delete_address(addre_id:int , db:Session , user:User):
    if is_admin(user):
      Deleteaddress = db.query(Addresses).filter(Addresses.id == addre_id).first()
      if not Deleteaddress:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="address not found")
      db.delete(Deleteaddress)
      db.commit()

      return {"message" : "address deleted"}
  
    else:
        deleteaddress=db.query(Addresses).filter(Addresses.user_id==user.id,Addresses.id==addre_id).first()
        if not deleteaddress:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="address not found")
        db.delete(deleteaddress)
        db.commit()

        return {"message" : "address deleted"}
    


# ----------------------CART ITEM---------------------------
# ---------------------CREATE CART-------------------------

def create_cartItem(body:CartItemSchema,user:User,db:Session):
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only active users can add items to cart")

    product = db.query(Product).filter(Product.id == body.pro_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if body.count>product.availability:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="stock not available")
    
    existing_product = db.query(CartItem).filter(CartItem.user_id == user.id,CartItem.pro_id == body.pro_id).first()

    if existing_product:
        
        existing_product.count += body.count
        if existing_product.count>product.availability:
             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="stock not available")

        db.commit()
        db.refresh(existing_product)

        return {
            "status": "ok", "message": "quantity updated in cart","cartItem": existing_product}

    else:
        new_cartItem=CartItem(
            count=body.count,
            user_id=user.id,
            pro_id=body.pro_id,
            pro_name=product.name,
            pro_price=product.price
        )

        db.add(new_cartItem)
        db.commit()
        db.refresh(new_cartItem)
        return{"status":"ok","message":"item added to cart successfully","cartItem":new_cartItem}

  
# ---------------------GET CART----------------------------

def get_cartItem(user:User,db:Session):
    if user.is_active and not user.is_seller :
        cart_item=db.query(CartItem).filter(CartItem.user_id==user.id).all()
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no item found")
        
        return{"cart_item":cart_item}
    
    if user.is_superuser:
        cart_item=db.query(CartItem).all()
        return {"cart_item":cart_item}
    
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="you cannot view the cart_item")
    
# ---------------------UPDATE CARTITEM----------------------------

def update_cartItem(pro_id:int,body:CartItemSchema,user:User,db:Session):
    if is_admin(user):
        cart_item = db.query(CartItem).filter(CartItem.pro_id == pro_id).first()
        if not cart_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="cart item not found")
        
        product = db.query(Product).filter(Product.id == pro_id).first()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")
        
        if body.count > product.availability:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Requested quantity not available")
        
        if body.count == 0:
            db.delete(cart_item)
            db.commit()
            return {"status": "ok", "message": "cart item removed"}
        
        cart_item.count = body.count
        db.commit()
        db.refresh(cart_item)
        return {"status":"ok","message":"cartItem updated successfully","cartItem":cart_item}
    

    if not user.is_active and not user.is_seller:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Only active users can update cartItems")
    
    cart_item=db.query(CartItem).filter(CartItem.pro_id==pro_id,CartItem.user_id==user.id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cart_item not found for this user")
    
    product=db.query(Product).filter(Product.id==pro_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="product not found")
    
    if body.count > product.availability:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Requested quantity not available")
    
    if body.count==0:
        db.delete(cart_item)
        db.commit()
        return {"status": "ok", "message": "cart item removed"}
    
    else:
    
        cart_item.count=body.count

        db.commit()
        db.refresh(cart_item)

        return{"status":"ok","message":"cartItem updated succesfully","cartItem":cart_item}


# ---------------------DELETE CARTITEM----------------------------

def delete_cartItem(cart_id:int,user:User,db:Session):
    if is_admin(user):
        deleteCart=db.query(CartItem).filter(CartItem.id==cart_id).first()
        if not deleteCart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cart not found")
        db.delete(deleteCart)
        db.commit()
        return {"status": "ok", "message": "cart deleted"}
    
    if user.is_active and not user.is_seller :
        deleteCart=db.query(CartItem).filter(CartItem.id==cart_id,CartItem.user_id==user.id).first()
        if not deleteCart:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="cart item found")
        
        db.delete(deleteCart)
        db.commit()
        return {"status": "ok", "message": "cart deleted"}
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cannot delete this cart item")

# ---------------------CREATE ORDER----------------------------   

def create_order(body: OrderSchema, user:User, db: Session ):
    
    if user.is_active:
    
      product = db.query(Product).filter(Product.id == body.pro_id).first()

      if not product :
        raise HTTPException(status_code=400, detail="Product not found")
      if product.in_stock < body.count:
          raise HTTPException(status_code=400, detail="Not suffficent stock")
          
      product.in_stock -= body.count

      new_order = Order(
        user_id=user.id,
        pro_id=body.pro_id,
        count=body.count,
        address=body.address,
        status=body.status
       )
      db.add(new_order)
      db.commit()
      db.refresh(new_order)

      return {"message": "Order placed", "order_id": new_order.id,"new_order":new_order} 
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized to create an order")

# ---------------------GET ORDER----------------------------

def get_orders(user:User, db: Session , user_id :int= None):
    
    if user.issuperuser:
        if user_id :
              orders = db.query(Order).filter(Order.user_id == user_id).all()
              
        orders = db.query(Order).all()

        return {"staus":"ok","Orders":orders} 
    
    if user.id!= Order.user_id  :
          raise HTTPException(status_code=401, detail="you are not allow to view others oreders")
    
    orders = db.query(Order).filter(Order.user_id == user.id).all()

    return {"staus":"ok","Orders":orders}    
       

# ---------------------UPDATE ORDER----------------------------       
       
def update_order(body:OrderSchema,db: Session, user:User,order_id:int= None, user_id :int= None ):
    
      if user.issuperuser:
            if order_id :
                  orders = db.query(Order).filter(Order.id == order_id).first()
            elif user_id : 
                  orders = db.query(Order).filter(Order.user_id == user_id).first() 
            if not orders :
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordes is not found")
            
            orders.status = body.status
            db.commit()
            return {"message": "Order updated"} 
            
      if user.id!= Order.user_id  :
          raise HTTPException(status_code=401, detail="you are not allow to update others oreders")
      
      orders = db.query(Order).filter(Order.user_id == user.id).first()
                  
      orders.status = body.status
      db.commit()
      return {"message": "Order status updated"}
    

# ---------------------DELETE ORDER----------------------------            
      
def delete_order(db: Session, user:User,order_id:int= None, user_id :int= None ):
    
    if user.issuperuser:
            if order_id :
                  orders = db.query(Order).filter(Order.id == order_id).first()
            elif user_id : 
                  orders = db.query(Order).filter(Order.user_id == user_id).first() 
            if not orders :
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordes is not found")
            db.delete(orders)
            db.commit()
            return {"message": "Order deleted"} 
            
    if user.id!= Order.user_id  :
          raise HTTPException(status_code=401, detail="you are not allow to update others oreders")
      
    orders = db.query(Order).filter(Order.user_id == user.id).first()
                  
    db.delete(orders)
    db.commit()
    return {"message": "Order deleted"}





