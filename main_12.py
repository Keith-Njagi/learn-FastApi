from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#  Basic Auth
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}