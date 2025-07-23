from fastapi import FastAPI, Query, Path
from enum import Enum
from typing import Annotated, Literal
import random
from pydantic import AfterValidator, Field, BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hello World"
    }


data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}

def check_if_valid(id: str):
    if not id.startswith(("isbn-", "imdb")):
        raise ValueError('Invalid ID format, harus tart dengan isbn- atau imdb- ')
    return id

@app.get("/books")
async def get_books(
    id: Annotated[str | None, AfterValidator(check_if_valid)] = None
):
    if id:
        item = data.get(id)
    else:
        id, item = random.choice(list(data.items()))
    return {
        "id": id,
        "name": item
    }


""" Optional but ada ketentuanya char tidak boleh lebih panjang dari 50 """
@app.get("/items/")
async def read_items(
    q: Annotated[str | None,Query(min_length=3,max_length=50, pattern="^fixquery$")] = None
):
    results = {
        "items": [
            {
                "item_id": "foo"
            },
            {
                "item_id": "bar"
            }
        ]
    }
    if q:
        results.update({"q": q})
    return results

""" query parameter that can appear multiple time
    = None bisa diganti untuk default value, misal = ['foo', 'bar']
 """
@app.get("/items-list/")
async def read_items_list(
    q: Annotated[
        list[str] | None,
        Query(
            title="Query String",
            description="Query string to search in the database",
            min_length=3,
            alias="item-query"
        )
    ] = None
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    
    return results


@app.get("/items/{item_id}")
async def read_item(
    item_id: Annotated[ int, Path(title="Id untuk itemnya", ge=1, le=1000) ],
    q: Annotated[str | None, Query(alias="item-query")] = None,
    size: Annotated[float, Query(gt=1, lt=10.5)] = None
):
    results = {
        "item_id": item_id
    }
    if q:
        results.update({"q": q})
    if size:
        results.update({"size": size})
    return results

@app.get("/users/me")
async def read_users_me(user: str):
    return {
        "user_id": "current_user"
    }

""" Misal ngakses users/me akan tetap menggunakan path yang pertama """
@app.get("/users/{user_id}")
async def read_users(user_id):
    return {
        "user_id": user_id
    }


""" Menggunakan parameter yang berupa enum """
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Hidup jokowi"
        }
    if model_name is ModelName.resnet:
        return {
            "model_name": model_name,
            "message": "pihak asing"
        }
    """ Bisa juga mencocokanya dengan string """
    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "kita ini bangsa yang besar"
        }
    
""" Parameter dengan file path """
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {
        "file_path": file_path
    }

""" Tes jika pake DB """

fake_items_db = [{"item_name": "foo"}, {"item_name": "bar"}, {"item_name": "bazz"}]

@app.get("/items-db")
async def read_item_db(skip:int = 0, limit: int = 10):
    return {
        "data": fake_items_db[skip: skip + limit],
        "skip": skip,
        "total": limit
    }

""" Optional Parameter """
@app.get("/item-optional/{item_id}")
async def read_item_ops(item_id: int, q: str | None = None, short: bool = False):
    item = {
        "id": item_id,
    }
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Ini adalah deskripsi"
            }
        )
    return item

""" Multiple path and query parameter """
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int,
    item_id: str,
    q: str | None = None,
    short: bool = False
):
    item = {
        "id": item_id,
    }
    if q:
        item.update({
            "q": q,
            "owner_id": user_id
            })
    if not short:
        item.update(
            {
                "description": "Ini adalah deskripsi"
            }
        )
    return item

""" Query paramter that required """
@app.get("/items-req-query/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {
        "item_id": item_id,
        "needy": needy
    }
    return item

""" pydantic model """

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items-pydantic")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

""" Kesimpulan parameter dan path:
    kalo parameter di declare ke path maka akan dianggap path,
    jika tidak maka akan dianggap query parameter
"""
@app.put("/items-pydantic/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q is not None:
        result.update({"q": q})
        
    return result



class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/quer-param-pydantic")
async def quer_param_pydantic(filter_query: Annotated[FilterParams, Query()]):
    return filter_query