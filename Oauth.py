'''Using OAuth (Open Authorization), we can identify which requests are valid.
The requests that have the token are the only valid requests
requests without tokens are invalid.'''



from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

'''OAuth with Password and Bearer
- first verify the user:
is the user name present in database
is the user password matching with the password stored in database (password is in hashed form)
- If Yes, generate the Bearer token
- else, User or password is wrong

Now if the authentication succeeds, use the token for further requests.
'''


'''OAuth with Password and JWT (JWT is a dense string formed from json object, this string has no space in it. 
To create this string, a secret key and an algorithm are required.)
- first verify the user:
is the user name present in database
is the user password matching with the password stored in database (password is in hashed form)
- If Yes, generate the JWT token
- else, User or password is wrong

Now if the authentication succeeds, use the token for further requests.
'''