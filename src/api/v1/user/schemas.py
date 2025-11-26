from pydantic import BaseModel, Field

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

class Fullname(BaseModel):
    name : str = Field(alias="first_name")
    family : str = Field(alias="last_name")

    model_config = {
        "populate_by_name": True
    }

class UsersResponse(BaseModel):
    id : int
    username : str
    fullname : Fullname
    tags : list[str] = Field(alias="labels")

    model_config = {
        "populate_by_name": True,
        "alias_generator": None
    }



class UserCreate(BaseModel):
    id  :int
    username : str = Field(..., min_length = 3, max_length = 10, description = "username must be between 3 to 10 character.")
    fullname : str 
    tags : list[str]
