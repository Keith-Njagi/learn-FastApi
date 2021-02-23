from typing import Dict, List, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int

class Stuff(BaseModel):
    name: str
    description: str


stuff = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

# Union or anyOf + status code
@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem], status_code=200)
async def read_item(item_id: str):
    return items[item_id]

# List of models + status code from starlette imported via fastAPI
@app.get("/items/", response_model=List[Stuff], status_code=status.HTTP_200_OK)
async def read_items():
    return items

# Response with arbitrary dict + status code from starlette imported via fastAPI
@app.get("/keyword-weights/", response_model=Dict[str, float], status_code=status.HTTP_200_OK)
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}