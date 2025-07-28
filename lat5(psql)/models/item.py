from sqlalchemy import Column, Integer, String
from config.database import Base
from pydantic import BaseModel

class ItemDict(BaseModel):
    name: str
    price: int

class Item(Base):
    __tablename__ = "items"

    name = Column(String, primary_key=True)
    price = Column(Integer)