'''While working with files, use the following steps to test with Postman
- As the below request is a POST request, there is a need of body
- Go in the form-data
- Add keys and change Text to File
- Upload the file
- Ref URL: https://www.postman.com/postman/postman-answers/documentation/t38ia1u/upload-a-file-via-post-request
'''

import os
import tempfile 
import uvicorn

from langchain_community.document_loaders import PDFPlumberLoader

from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse



app = FastAPI()


@app.post("/files/")
async def create_files(
    files: Annotated[list[bytes], File(description="Multiple files as bytes")],
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(
    files: Annotated[
        list[UploadFile], File(description="Multiple files as UploadFile")
    ],
):
    for file in files[:1]:
        suffix = os.path.splitext(file.filename)[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # Use PDFPlumberLoader with the file path
        loader = PDFPlumberLoader(tmp_path)
        docs = loader.load()
        print(docs[0]) # print statements work only when you use fastapi in dev environment (fastapi dev fileupload.py)

    return {"filenames": [file.filename for file in files], "content": docs[0].page_content}


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

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=5000)