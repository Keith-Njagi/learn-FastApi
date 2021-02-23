from typing import List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: List[str] = []

# Multiple Models
'''
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None
'''
# To reduce duplication as above:
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db

#  Response Model + tags(used in OpenAPI documentation)
@app.post("/user/", response_model=UserOut, tags=['users'])
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
    
# Response Model
# it can be a Pydantic model, but it can also be, e.g. a list of Pydantic models, like List[Item].
# tags + summary + description + doc strings documentation + response description
# You can use either description or doc strings but not both for OpenAPI documentation
@app.post("/items/", 
    response_model=Item, 
    status_code=201,
    tags=['items'],
    summary="Create an item",
    # description="Create an item with all the information, name, description, price, tax and a set of unique tags",
    response_description="The created item",
    )
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# Excluding default values in the response. e.g: description, tax, tags
'''
You can also use:

response_model_exclude_defaults=True
response_model_exclude_none=True

as described in the Pydantic docs for exclude_defaults and exclude_none.
'''
@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True, tags=['items'])
async def read_item(item_id: str):
    return items[item_id]

# Deprecate a path operation
@app.get("/elements/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]