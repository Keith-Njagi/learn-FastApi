from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.encoders import jsonable_encoder # Converts a data type (like a Pydantic model) to something compatible with JSON (like a dict, list, etc).
from fastapi.exceptions import RequestValidationError
from fastapi.responses import  JSONResponse, PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel

# https://fastapi.tiangolo.com/tutorial/handling-errors/

app = FastAPI()

# Overide the HTTPException Error Handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Overide the Request Validation Exceptions 
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

# Comment this out to be able to Overide the Request Validation Exceptions above
# Use the RequestValidationError body
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

# Re-use FastAPI's exception handlers
# In this example, you are just printing the error with a very expressive message.
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)

# Re-use FastAPI's exception handlers
# In this example, you are just printing the error with a very expressive message.
# Comment this out to be able to use the RequestValidationError body above
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

# Use the RequestValidationError body
class Item(BaseModel):
    title: str
    size: int

# Use the RequestValidationError body
@app.post("/items/")
async def create_item(item: Item):
    return item


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")
    return {"item_id": item_id}