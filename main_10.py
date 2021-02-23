from typing import List, Optional

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder # Converts a data type (like a Pydantic model) to something compatible with JSON (like a dict, list, etc).
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, tags=['items'])
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item, tags=['items'], response_description='Updated Item')
async def update_item(item_id: str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

#  To use patch(partial updates), you need to set all the values in the pydantic model to optional
# To distinguish from the models with all optional values for updates and models with required values for creation, you can use the ideas described in main_5.py(Extra models).
@app.patch("/items/{item_id}", response_model=Item, tags=['items'], response_description='Updated Item')
async def update_item(item_id: str, item: Item):
    stored_item_data = items[item_id]
    stored_item_model = Item(**stored_item_data)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data) # See file: try_1.py to see how Pydantic's update parameter is used
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item