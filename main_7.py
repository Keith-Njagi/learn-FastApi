from typing import List

from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()
'''
When you need to receive form fields instead of JSON, you can use Form.

Info

To use forms, first install python-multipart.

E.g. pip install python-multipart.

You can declare multiple File and Form parameters in a path operation, 
but you can't also declare Body fields that you expect to receive as JSON, 
as the request will have the body encoded using multipart/form-data instead of application/json.

This is not a limitation of FastAPI, it's part of the HTTP protocol.

Use File and Form together when you need to receive data and files in the same request.
'''

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


@app.post("/file/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}

# UploadFile uses a "spooled" file:
# A file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # UploadFile methods (read(size), write(data), and seek(offset:int)), are all async functions and you need to await them
    contents = await myfile.read()
    return {"filename": file.filename}

# Multiple file uploads
@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}

# Multiple file uploads
@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post("/files_and_form/")
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }