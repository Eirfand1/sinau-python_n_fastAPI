from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException

def get_or_404(db: Session, model, id: int, name="Data"):
    obj = db.query(model).filter(model.id == id).first()
    if not obj:
        raise HTTPException(404, f"{name} Not Found")
    return obj

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
    mahasiswa = get_or_404(db, models.Mahasiswa, id, "Mahasiswa")
    return mahasiswa

def update_mahasiswa(db: Session, data: schemas.MahasiswaUpdate, id: int):
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
    obj = models.Dosen(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_dosen_all(db: Session):
    return db.query(models.Dosen).all()

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
