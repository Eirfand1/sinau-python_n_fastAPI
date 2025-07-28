from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from schemas.item import ItemBase
import services.item as ItemService
import models.item as ItemModel


ItemModel.Base.metadata.create_all(bind=engine)
itemrouter = APIRouter()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally: 
        session.close

@itemrouter.get("/items/", response_model=List[ItemBase])
def read_items(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session)

):
    items = ItemService.get_items(db=db, skip=skip, limit=limit)
    return items

@itemrouter.get("/items/{name}", response_model=ItemBase)
def read_item(name: str, db: Session = Depends(get_session)):
    item = ItemService.get_item_by_name(db=db, name=name)
    return item
