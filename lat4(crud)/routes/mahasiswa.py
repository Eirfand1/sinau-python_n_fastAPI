from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.WebResponse[schemas.MahasiswaOut])
def create_mahasiswa(mhs: schemas.MahasiswaCreate, db: Session = Depends(get_db)):
    mahasiswa = crud.create_mahasiswa(db, mhs)
    return schemas.WebResponse(success=True, data=mahasiswa)

@router.get("/", response_model=schemas.WebResponse[list[schemas.MahasiswaOut]])
def list_mahasiswa(db: Session = Depends(get_db)):
    data = crud.get_mahasiswa_all(db)
    return schemas.WebResponse(success=True, data=data)

@router.get("/{id}", response_model=schemas.WebResponse[schemas.MahasiswaOut])
def find_mahasiswa(db: Session = Depends(get_db), id: int = id):
    data = crud.find_mahasiswa(db, id)
    return schemas.WebResponse(success=True, data=data)

