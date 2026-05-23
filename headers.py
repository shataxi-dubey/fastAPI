from fastapi import FastAPI, Header

from pydantic import BaseModel

from typing import Annotated

app = FastAPI()

class MultipleHeader(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    # x_tag: list[str] = []

@app.get('/headers')
def get_headers(headers: Annotated[MultipleHeader, Header()]):
    return headers
