import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    a = "a"
    b = "b" + a
    return {"hello world": b}

# You can connect the debugger in your editor, for example with Visual Studio Code or PyCharm.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)