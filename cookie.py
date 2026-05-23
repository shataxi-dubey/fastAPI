'''While working with cookies, use the following steps to test with Postman
- As the below request is a GET request, there is no need of json body
- Add cookies in the "cookies" section
- each cookie will have the syntax of form "Cookie_1=value; Path=/; Expires=Thu, 06 Aug 2026 05:59:35 GMT;"
- Replace Cookie_1 with cookie parameter name and value with the cookie value
- Expires tells when the cookie will expire
- Ref URL: https://learning.postman.com/docs/sending-requests/response-data/cookies/#send-cookies-with-a-request
'''

from fastapi import FastAPI, Cookie

from typing import Annotated

from pydantic import BaseModel

class Cookies(BaseModel):
    session_id: int
    f_tracker: str|None = None
    g_tracker: str|None = None

app = FastAPI()

@app.get("/ads")
def get_ads(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

@app.get("/items")
def read_items(cookies: Annotated[Cookies, Cookie()]):
    return cookies


