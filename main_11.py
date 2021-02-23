from typing import Optional

from fastapi import Cookie, Depends, FastAPI, Header
from fastapi.exceptions import HTTPException

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# Dependancies based on functions
async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

# Dependancies based on classes
class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

# Dependancy inheritance: First dependancy
def query_extractor(q: Optional[str] = None):
    return q

# Dependancy inheritance: Second dependancy
def query_or_cookie_extractor(q: str = Depends(query_extractor), last_query: Optional[str] = Cookie(None)):
    if not q:
        return last_query
    return q

# Add dependencies to the path operation decorator
# Dependancy values (if they return any) won't be passed to your path operation function.
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
# Add dependencies to the path operation decorator
# Dependancy values (if they return any) won't be passed to your path operation function.
async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# Trial dependancy for calling multiple times without caching
class Increment:
    def __init__(self, number:Optional[int] = None):
        self.number = number

    def minus(self):
        if self.number:
            self.number = self.number - 1
            return self.number
        return 0 

@app.get('/increment/')
async def increment_items(number:Increment = Depends()):
    my_dict = {}
    my_number = number
    while my_number.number != 0:
        item = {number.number:'item'}
        my_dict.update(item)
        my_number.minus()
    return my_dict

# Dependancies based on functions
# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons

# Dependancies based on classes
@app.get("/items/", description='Dependancies based on classes')
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)): # To reduce this repetition:
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

@app.get("/queries/", description='Dependancies inheritance based on functions')
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
'''
In an advanced scenario where you know you need the dependency to be called at every step 
(possibly multiple times) in the same request instead of using the "cached" value, 
you can set the parameter use_cache=False when using Depends:

@app.get("/needy/", )
async def needy_dependency(fresh_value: str = Depends(get_value, use_cache=False)):
    return {"fresh_value": fresh_value}
'''

@app.get("/users/", description='Dependancies based on functions')
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

# Add dependencies to the path operation decorator
# Dependancy values (if they return any) won't be passed to your path operation function.
@app.get("/tokenized_items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

'''
FastAPI supports dependencies that do some extra steps after finishing.

To do this, use yield instead of return, and write the extra steps after.

Make sure to use yield one single time.

For this to work, you need to use Python 3.7 or above, or in Python 3.6, install the "backports":

pip install async-exit-stack async-generator

e.g:

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

Only the code prior to and including the yield statement is executed before sending a response: ie. from 'async def' to 'yield db'
The yielded value is what is injected into path operations and other dependencies: ie. yield db
The code following the yield statement is executed after the response has been delivered: ie. finally:

Ineritance:

async def dependency_a():
    dep_a = generate_dep_a()
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = generate_dep_b()
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = generate_dep_c()
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)
'''