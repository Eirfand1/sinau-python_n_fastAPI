from pydantic import BaseModel
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class WebResponse(BaseModel, Generic[T]):
    success: bool
    data: T

class MahasiswaBase(BaseModel):
    nama: str
    nim: str

class MahasiswaCreate(MahasiswaBase):
    nama: Optional[str] = None
    nim: Optional[str] = None

class MahasiswaUpdate(MahasiswaBase):
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

class DosenUpdate(DosenBase):
    nama: Optional[str] = None
    nip: Optional[str] = None

class DosenOut(DosenBase):
    id: int
    class Config:
        from_attributes = True
