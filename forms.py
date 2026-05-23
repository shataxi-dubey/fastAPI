from fastapi import FastAPI, Form

from pydantic import BaseModel

from typing import Annotated

app = FastAPI()

class Formfields(BaseModel):
    username: str
    password: str


@app.get('/login')
def login(data: Annotated[Formfields, Form()]):
    return data