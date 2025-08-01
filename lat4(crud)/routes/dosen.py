from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas
import crud
from database import get_db
from typing import Optional

router = APIRouter()

@router.post("/", response_model=schemas.WebResponse[schemas.DosenOut], status_code=201)
def create_dosen(
    dsn: schemas.DosenCreate,
    db: Session = Depends(get_db),
):
    dosen = crud.create_dosen(db, dsn) 
    return schemas.WebResponse(success=True, data=dosen)

@router.get("/", response_model=schemas.PaginateWebResponse[list[schemas.DosenOut]])
def list_dosen(
    db: Session = Depends(get_db),
    skip: Optional[int] = 0,
    limit: Optional[int] = 10
):
    dosen =  crud.get_dosen_all(db, skip, limit)
    return schemas.PaginateWebResponse(success=True, data=dosen, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.WebResponse[schemas.DosenOut])
def find_dosen(db: Session = Depends(get_db), id: int = id):
    dosen = crud.find_dosen(db, id) 
    return schemas.WebResponse(success=True, data=dosen)

@router.put("/{id}", response_model=schemas.WebResponse[schemas.DosenOut])
def update_dosen(dsn: schemas.DosenUpdate, db: Session = Depends(get_db), id: int = id):
    dosen = crud.update_dosen(db, dsn, id)
    return schemas.WebResponse(success=True, data=dosen)

@router.delete("/{id}", response_model=schemas.WebResponse[schemas.DosenOut])
def remove_dosen(db: Session = Depends(get_db), id: int = id):
    dosen = crud.remove_dosen(db, id)
    return schemas.WebResponse(success=True, data=dosen)