from pydantic import BaseModel, Field

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