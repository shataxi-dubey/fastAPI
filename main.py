from fastapi import FastAPI, Query, Body

from typing import Union, Annotated

from pydantic import BaseModel
from enum import Enum

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
    tax: float

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


class Product(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None
    tax: float

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item": item, "item_id": item_id}

@app.get('/products')
def get_productdetails(q: Annotated[Product, Query()]):
    return q

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): # ModelName is a Enum which restricts the number of model names
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images", "modelnamevalue": model_name.value}

    return {"model_name": model_name, "message": "Have some residuals"}

@app.get("/filepath/{filename:path}") # example path: /filepath//home/test.txt
def get_filename(filename: str):
    return {"filename": filename}


# use of query parameters, query parameters are not part of URIs
@app.get('/usequeryparameter/{uri_param}')  # example http://127.0.0.1:8000/usequeryparameter/2?query=adsdfdfgd
def get_query_params(uri_param: int, query1: str|None = None, query2: str|None = None):
    if query1 and query2:
        return {"Parameter passed in URI":uri_param, "Query in the URI": query1, "Query in the URI": query2 }
    else:
        return {"Parameters passed in URI": uri_param}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = dict(item)
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict