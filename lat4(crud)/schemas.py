from pydantic import BaseModel, EmailStr
from typing import TypeVar, Generic, Optional

T = TypeVar("T")

class WebResponse(BaseModel, Generic[T]):
    success: bool
    data: T

class PaginateWebResponse(WebResponse[T], Generic[T]):
    skip: Optional[int] = None
    limit: Optional[int] = None

class MahasiswaBase(BaseModel):
    nama: str
    nim: str
    email: EmailStr
    prodi: str

class MahasiswaCreate(MahasiswaBase):
    nama: Optional[str] = None
    nim: Optional[str] = None
    email: Optional[EmailStr] = None
    prodi: Optional[str] = None

class MahasiswaUpdate(MahasiswaBase):
    pass

class MahasiswaOut(MahasiswaBase):
    id: int
    class Config:
        from_attributes = True

class DosenBase(BaseModel):
    nama: str
    nip: str
    email: EmailStr
    prodi: str

class DosenCreate(DosenBase):
    pass

class DosenUpdate(DosenBase):
    nama: Optional[str] = None
    nip: Optional[str] = None
    email: Optional[EmailStr] = None
    prodi: Optional[str] = None

class DosenOut(DosenBase):
    id: int
    class Config:
        from_attributes = True

class ShortUrlBase(BaseModel):
    url: str
    shorted_url: str

class ShortUrlOut(ShortUrlBase):
    id: int
    class Config:
        from_attributes: True

class ShortUrlIn(ShortUrlBase):
    class Config: 
        fields = {
            "shorted_url": str
        }

