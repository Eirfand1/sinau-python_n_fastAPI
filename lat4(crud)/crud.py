from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException
from typing import Optional
from schemas import MahasiswaOut, DosenOut, ShortUrlBase

def get_or_404(db: Session, model, id: int, name="Data"):
    obj = db.query(model).filter(model.id == id).first()
    if not obj:
        raise HTTPException(404, f"{name} Not Found")
    return obj

def create_mahasiswa(db: Session, data: schemas.MahasiswaCreate) -> MahasiswaOut:
    obj = models.Mahasiswa(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_mahasiswa_all(db: Session, skip: Optional[int] = 0, limit: Optional[int] = 10) -> list[MahasiswaOut]:
    mahasiswa = db.query(models.Mahasiswa).limit(limit).offset(skip)
    return mahasiswa

def find_mahasiswa(db: Session, id: int) -> MahasiswaOut:
    mahasiswa = get_or_404(db, models.Mahasiswa, id, "Mahasiswa")
    return mahasiswa

def update_mahasiswa(db: Session, data: schemas.MahasiswaUpdate, id: int) -> MahasiswaOut:
    mahasiswa = get_or_404(db, models.Mahasiswa, id, "Mahasiswa")
    for key, value in data.model_dump().items():
        setattr(mahasiswa, key, value)
    
    db.commit()
    db.refresh(mahasiswa)
    return mahasiswa

def remove_mahasiswa(db: Session, id: int):
    mahasiswa = get_or_404(db, models.Mahasiswa, id, "Mahasiswa")
    
    db.delete(mahasiswa)
    db.commit()
    return mahasiswa

def find_dosen(db: Session, id: int):
    dosen= get_or_404(db, models.Dosen, id, "Dosen")
    return dosen

def create_dosen(db: Session, data: schemas.DosenCreate):
    obj = models.Dosen(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_dosen_all(db: Session, skip: Optional[int] = 0, limit: Optional[int] = 10):
    return db.query(models.Dosen).offset(skip).limit(limit).all()

def update_dosen(db: Session, data: schemas.DosenUpdate, id: int):
    dosen = get_or_404(db, models.Dosen, id, "Dosen")
    
    for key, value in data.model_dump().items():
        setattr(dosen, key, value)

    db.commit()
    db.refresh(dosen)
    return dosen

def remove_dosen(db: Session, id: int):
    dosen = get_or_404(db, models.Dosen, id, "Dosen")
    
    db.delete(dosen)
    db.commit()
    return dosen


def short_url(db: Session, data: ShortUrlBase, server_url: str):
    obj = models.Shorturl(**data.model_dump())
    db.add(obj)
    db.commit()
    return obj
    
