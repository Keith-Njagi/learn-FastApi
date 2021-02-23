from enum import Enum
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

# If you have a path operation that receives a path parameter, 
# but you want the possible valid path parameter values to be predefined, 
# you can use a standard Python Enum.
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# The same as when declaring query parameters, 
# when a model attribute has a default value, it is not required. 
# Otherwise, it is required. Use None to make it just optional.
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
async def root():
    return {"message": "Hello World"}
'''
Path parameters -> example.com/items/10 -> 10 is a path parameter
Query parameters -> example.com/items/?skip=0&limit=10 -> skip & limit are query parameters
Request body -> to be expected from forms and such -> these do not apear in the URL
'''
# Query Parameters
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10): # Query Parameters
    return fake_items_db[skip : skip + limit]

# Declare Model as a parameter (request body)
# Use the model
@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

"""
Required Query parameters
Optional parameters
Query parameter type conversion

needy, a required str.
skip, an int with a default value of 0.
limit, an optional int.
q, an optional str.
short, a bool with a default value of False
"""
@app.get("/items/{item_id}")
async def read_item(item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# Request body + path + query parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# Multiple path and query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item

# Enum Models
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == ModelName.lenet.value: # or if model_name.value ==  "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# File paths
# e.g: /files/home/johndoe/myfile.txt
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}