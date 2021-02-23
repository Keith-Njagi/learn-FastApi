from typing import Dict, List, Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl # we  declare it to be instead of a str, a Pydantic's HttpUrl:
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None 
    # tags: list = [] # You can define an attribute to be a subtype. For example, a Python list:
    # tags: List[str] = [] # to declare lists with internal types, or "type parameters":
    tags: Set[str] = set() # Set types
    # image: Optional[Image] = None # Nested Models
    images: Optional[List[Image]] = None # You can also use Pydantic models as subtypes of list, set, etc:
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }
'''
    declaring extra JSON Schema information using Config and schema_extra within the Item(BaseModel):

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

or using example as below:

class Item(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)

or passing them as a request body in your route as:

item: Item = Body(..., example={"name": "Foo","description": "A very nice Item","price": 35.4,"tax": 3.2,},),

'''

# arbitrarily deeply nested models:
class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

# Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images

# Bodies of arbitrary dicts
# In this case, you would accept any dict as long as it has int keys with float values:
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights