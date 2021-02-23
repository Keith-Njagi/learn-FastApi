from typing import Optional

from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel, Field

# Field functions the same as Query, Path and Body to declare additional validation and metadata in Pydantic models
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, title="The description of the item", max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None

app = FastAPI()

# Additional validation (Using Query class -> Here we set the parameter max_length to 50)
# async def read_items(q: str = Query(..., min_length=3)): -> Here q is a required parameter declared so by the ... AKA Ellipsis
# async def read_items(q: Optional[List[str]] = Query(None)): -> Query parameter list (http://localhost:8000/items/?q=foo&q=bar)
'''
To declare a query parameter with a type of list, 
like in the example above, you need to explicitly use Query, 
otherwise it would be interpreted as a request body.
'''
# async def read_items(q: List[str] = Query(["foo", "bar"])): -> Default list values
# async def read_items(q: list = Query([])): -> Using list directly
# Query(None, title="Query string", description="Query string for the items", min_length=3) -> title & description is just metadata for OpenAPI documentation
# Query(None, alias="item-query") -> item-query is what will be used in the URL
# Query(None, title="Query string", deprecated=True) -> Tells OPenAPI docs the parameter is deprecated
@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")): # or Query("fixedquery", min_length=3, max_length=50)
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

'''
Python will complain if you put a value with a "default" before a value that doesn't have a "default".

1 is python's recommended order by having the value without a default (the query parameter q) first. 
2 helps us order by seting the parameters as key word arguments(key value pairs)/kwargs, even if they don't have a default value.

1. async def read_items(q: str, item_id: int = Path(..., title="The ID of the item to get")):
2. async def read_items(*, item_id: int = Path(..., title="The ID of the item to get"), q: str): 
'''
# lt: less than
# gt: greater than
# le: less than or equal
# ge: greater than or equal to

# item_id: int = Path(..., title="The ID of the item to get", ge=1)
# Here, with ge=1, item_id will need to be an integer number "*g*reater than or *e*qual" to 1.

# item_id: int = Path(..., title="The ID of the item to get", gt=0, le=1000)

# for floats & query parameters
# size: float = Query(..., gt=0, lt=10.5)
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# But you can also declare multiple body parameters, e.g. item and user:
'''
The same way there is a Query and Path to define extra data for query and path parameters, 
FastAPI provides an equivalent Body.

For example, extending the previous model, 
you could decide that you want to have another key "importance" in the same body, besides the item and user.

Data expected would look like:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
Body also has all the same extra validation and metadata parameters as Query,Path and others you will see later.
'''

'''
But if you want it to expect a JSON with a key item and inside of it the model contents, 
as it does when you declare extra body parameters, you can use the special Body parameter embed:

item: Item = Body(..., embed=True)

In this case FastAPI will expect a body like:

{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
instead of:

{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
'''
@app.put("/items/update/{item_id}")
async def update_items(item_id: int, item: Item, user: User, importance: int = Body(..., gt=0), q: Optional[str] = None):
    results = {"item_id": item_id, "item": item, "user": user}
    return results