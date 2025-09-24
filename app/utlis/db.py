from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine

Base=declarative_base()

db_url="sqlite:///e-commerce.db"

db_init=create_engine(db_url)
localSession=sessionmaker(bind=db_init)

def get_db():
    db=localSession()
    try:
        yield db
    finally:
        db.close()