from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db
from typing import Optional

router = APIRouter()

@router.post("/", response_model=schemas.WebResponse[schemas.MahasiswaOut], status_code=201)
def create_mahasiswa(mhs: schemas.MahasiswaCreate, db: Session = Depends(get_db)):
    mahasiswa = crud.create_mahasiswa(db, mhs)
    return schemas.WebResponse(success=True, data=mahasiswa)

@router.get("/", response_model=schemas.PaginateWebResponse[list[schemas.MahasiswaOut]])
def list_mahasiswa(
    db: Session = Depends(get_db),
    skip: Optional[int] = 0,
    limit: Optional[int] = 10
):
    mahasiswa = crud.get_mahasiswa_all(db,skip, limit)
    return schemas.PaginateWebResponse(success=True, data=mahasiswa, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.WebResponse[schemas.MahasiswaOut])
def find_mahasiswa(db: Session = Depends(get_db), id: int = id):
    mahasiswa = crud.find_mahasiswa(db, id)
    return schemas.WebResponse(success=True, data=mahasiswa)

@router.put("/{id}", response_model=schemas.WebResponse[schemas.MahasiswaOut])
def update_mahasiswa(mhs: schemas.MahasiswaUpdate, db: Session = Depends(get_db), id: int = id):
    mahasiswa = crud.update_mahasiswa(db, mhs,id)
    return schemas.WebResponse(success=True, data=mahasiswa)

@router.delete("/{id}", response_model=schemas.WebResponse[schemas.MahasiswaOut])
def remove_mahasiswa(db: Session = Depends(get_db), id: int = id):
    mahasiswa = crud.remove_mahasiswa(db, id)
    return schemas.WebResponse(success=True, data=mahasiswa)