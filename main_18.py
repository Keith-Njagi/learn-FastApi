from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}

# In a real use case, anything from this point would be in a different file
# Because our file is main_18.py, the test file would be test_main_18.py
# then we would do a: from .main import app
client = TestClient(app)

# Tests
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}