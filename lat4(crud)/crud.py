from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException

def create_mahasiswa(db: Session, data: schemas.MahasiswaCreate):
    obj = models.Mahasiswa(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_mahasiswa_all(db: Session):
    mahasiswa = db.query(models.Mahasiswa).all()
    return mahasiswa

def find_mahasiswa(db: Session, id: int):
    mahasiswa = db.query(models.Mahasiswa).filter(models.Mahasiswa.id == id).first()
    if not mahasiswa:
        raise HTTPException(404, detail="Mahasiswa Not Found")

    return mahasiswa

def find_dosen(db: Session, id: int):
    dosen= db.query(models.Dosen).filter(models.Dosen.id == id).first()
    if not dosen:
        raise HTTPException(404, detail="Dosen not found")
    return dosen

def create_dosen(db: Session, data: schemas.DosenCreate):
    obj = models.Dosen(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_dosen_all(db: Session):
    return db.query(models.Dosen).all()
