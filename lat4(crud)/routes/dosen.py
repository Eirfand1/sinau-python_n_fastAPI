from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.WebResponse[schemas.DosenOut])
def create_dosen(dsn: schemas.DosenCreate, db: Session = Depends(get_db)):
    dosen = crud.create_dosen(db, dsn) 
    return schemas.WebResponse(success=True, data=dosen)

@router.get("/", response_model=list[schemas.DosenOut])
def list_dosen(db: Session = Depends(get_db)):
    return crud.get_dosen_all(db)

@router.get("/{id}", response_model=schemas.WebResponse[schemas.DosenOut])
def find_dosen(db: Session = Depends(get_db), id: int = id):
    dosen = crud.find_dosen(db, id) 
    return schemas.WebResponse(success=True, data=dosen)