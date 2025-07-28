from typing import List
from sqlalchemy.orm import Session
from models.item import Item
from fastapi import HTTPException

def get_item_by_name(db: Session, name: str) -> Item:
    items = db.query(Item).filter(Item.name == name).first()
    if not  items:
        raise HTTPException(404, "Items not found")
    return items

def get_items(db: Session, skip: int = 0, limit: int = 0) -> List[Item]:
    items = db.query(Item).offset(skip).limit(limit).all()
    return items