from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T")

class WebResponse(BaseModel, Generic[T]):
    success: bool
    data: T

class MahasiswaBase(BaseModel):
    nama: str
    nim: str

class MahasiswaCreate(MahasiswaBase):
    pass

class MahasiswaOut(MahasiswaBase):
    id: int
    class Config:
        from_attributes = True

class DosenBase(BaseModel):
    nama: str
    nip: str

class DosenCreate(DosenBase):
    pass

class DosenOut(DosenBase):
    id: int
    class Config:
        from_attributes = True
