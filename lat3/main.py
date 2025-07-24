from fastapi import FastAPI, Query, Path, Body, Cookie, Header, Response
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Annotated
import random
from pydantic import AfterValidator
from model import ModelName, Item, User, FilterParams, Item2, Offer, Image, Item3, Cookies, CommondHeader, Item4, UserIn, UserOut
from uuid import UUID
from datetime import datetime, time, timedelta


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

    parameter dengan union Model = None bisa untuk optional
"""
@app.put("/items-pydantic/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="ID item", ge=0, le=1000)],
    item: Item | Item = None,
    q: str | None = None,
):
    result = {"item_id": item_id, **item.model_dump()}
    if q is not None:
        result.update({"q": q})
        
    return result

""" Multiple body, perlu item dan user """
@app.put("/items-update2/{item_id}")
async def update_item2(
    *,
    item_id: int, 
    item: Item,
    user: User,
    importance: Annotated[int, Body()],
    q: str | None = None
):
    result = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance
    }
    if q:
        result.update({"q": q})
    return result


""" Agar body request json expect sebuah key """
@app.put("/items-update3/{item_id}")
async def update_item3( 
    item_id: int,
    item: Annotated[Item, Body(embed=True)]
):
    result =  {
        "item_id": item_id,
        "item": item
    }
    return result

@app.put("/items-update4/{item_id}")
async def update_item4(
    item_id: int,
    item: Annotated[
        Item2,
        Body(
            examples=[
                {
                    "name": "kinderjoy",
                    "description": "deskripsi produk",
                    "price": 10000,
                    "tax": 110
                },
                {
                    "name": "shampo lifeboy",
                    "price": 20000,
                },
                {
                    "name": "Kahf Facewash",
                    "price": 50000,
                }
            ]
        )
    ]
):
    result = {
        "item_id": item_id,
        "item": item
    }
    return result


@app.put("/items-update6/{item_id}")
async def update_item6(
    item_id: int,
    item: Annotated[
        Item2,
        Body(
           openapi_examples={
               "normal": {
                   "summary": "Contoh normal",
                   "description": "Normal item yang akan work",
                   "value": {
                       "name": "sebuah item",
                       "description": "Sebuah Item",
                       "price": 50000,
                       "tax": 550
                   },
               },
               "converted" : {
                   "summary": "contoh untuk konversi string ke int otomatis",
                   "description": "FastApi bisa convert dari string ke int secara otomatis",
                   "value": {
                       "name": "sebuah item2",
                       "price": "70000"
                   },
               },
               "invalid": {
                   "summary": "sebuah item yang tidak sah",
                   "value": {
                       "name": "sebuah item3",
                       "price": "sepuluh ribu"
                   }
               }
           }
        )
    ]
):
    result = {
        "item_id": item_id,
        "item": item
    }
    return result



@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.get("/quer-param-pydantic")
async def quer_param_pydantic(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

""" Body of pure list """
@app.post("/image/multiple")
async def create_multiple_images(images: list[Image]):
    return images

@app.post("/index-weight")
async def create_index_weights(weights: dict[int, float]):
    return weights

@app.put("/items5/{item_id}")
async def update_item5(item_id: int, item: Item3):
    results = {
        "item_id": item_id,
        "item": item
    }
    return results

@app.put("/extra-datatype")
async def extra_datatype(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration
    }


""" cookies parameter """
@app.get("/cookie-param")
async def cookie_param(ads_id: Annotated[str | None, Cookie()] = None):
    return {
        "ads_id": ads_id
    }

""" Header param """
@app.get("/header-param")
async def header_param(user_agent: Annotated[str | None, Header()] = None):
    return {
        "User-Agent": user_agent
    }

@app.get("/strage-header")
async def strange_items(
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
):
    return {
        "Authorization": strange_header
    }

@app.get("/duplicate-header")
async def duplicate_header(x_token: Annotated[list[str] | None, Header()] = None):
    return {
        "X-Token values": x_token
    }

""" Cookie param model """
@app.get("/cookie-param-model")
async def cookie_param_model(cookies: Annotated[Cookies, Cookie()]):
    return cookies

""" Header param model """
@app.get("/header-param-model")
async def header_param_model(header: Annotated[CommondHeader, Header()]):
    return header


""" Response dengan kembalian model tipe """
@app.get("/response-model")
async def response_model() -> list[Item4]:
    return [
        Item4(name="Dor dor ajaib", price=1000000),
        Item4(name="Plumbus", price=2000000)
    ]

""" atau bisa juga gini """

@app.get("/response-model2", response_model=list[Item4])
async def response_model2() -> any:
    return [
        Item4(name="Dor dor ajaib", price=1000000),
        Item4(name="Plumbus", price=2000000)
    ]

""" request tetap menggunakan model userin tetapi response menggunakan user out """
@app.post("/user2", response_model=UserOut)
async def create_user2(user: UserIn) -> any:
    return user

""" Returning response directly """
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com")
    return JSONResponse(content={"message": "Redirect ke url youtube"})
