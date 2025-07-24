from pydantic import AfterValidator, Field, BaseModel, HttpUrl, EmailStr
from enum import Enum
from typing import Literal

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="deskripsi tentang item", max_length=20
    )
    price: float = Field(gt=0, description="Harus lebih besar dari pada 0")
    tax: float | None = None


class Image(BaseModel):
    """ Tipe khusus untuk validasi kalo itu adalah sebuah url """
    url: HttpUrl
    name: str

class Item2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    """ list = [] mengijinkan item yang sama """
    """ tags: list = [] """
    """ Pake set data yang kembar akan dihilangkan """
    tags: set[str] = set()
    """ Nested bisa begini juga ngambil dari model lain """
    image: list[Image] | None = None

class Item3(BaseModel):
    name: str
    description: str
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Abcd",
                    "description": "Sebuah item",
                    "price": 10000,
                    "tax": 110
                }
            ]
        }
    }

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item2]

class User(BaseModel):
    username: str
    full_name: str | None

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


class Cookies(BaseModel):
    """ Selain yang didefinisikan di model ini bakal gk diijinkan """
    model_config = {"extra": "forbid"}

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


class CommondHeader(BaseModel):
    """ jika ada header lain yang tidak didefinisikan di model akan forbid """
    """ model_config = {"extra": "forbid"} """

    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []


class Item4(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None
