from typing import Optional

from fastapi import BackgroundTasks, Depends, FastAPI
from fastapi.staticfiles import StaticFiles # To mount static files like in Django

# Create metadata for tags
# The order of each tag metadata dictionary also defines the order shown in the docs UI.
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

# If you want to disable the OpenAPI schema completely you can set openapi_url=None, 
# that will also disable the documentation user interfaces that use it.
# You can also use for Swagger UI url: docs_url="/documentation" or to disable docs_url=None,
# and for ReDoc url: redoc_url="myurl" or to disable redoc_url=None
app = FastAPI(openapi_tags=tags_metadata, openapi_url="/api/v1/openapi.json")

# Mounting/Using StaticFiles
# "Mounting" means adding a complete "independent" application in a specific path, 
# that then takes care of handling all the sub-paths.
'''
The first "/static" refers to the sub-path this "sub-application" will be "mounted" on. 
So, any path that starts with "/static" will be handled by it.

The directory="static" refers to the name of the directory that contains your static files.

The name="static" gives it a name that can be used internally by FastAPI.

All these parameters can be different than "static", adjust them with the needs and specific details of your own application.
'''
app.mount("/static", StaticFiles(directory="static"), name="static")

# Using BackgroundTasks
# Create a task function
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)
        print('===================')
        print(f'Printed: {message}')

# Dependency Injection
def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


@app.post("/send-notification/{email}")
async def send_notification(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}

# metadata for tags
@app.get("/users/", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]

# metadata for tags
@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]