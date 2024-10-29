from pydantic import BaseModel, Field, EmailStr
from typing_extensions import Annotated
from typing import Union


class RecommendationOut(BaseModel):
    ISBN: str
    TITLE: str
    PUBLICATION_YEAR: int
    PUBLISHER: str
    AVERAGE: float
    CORRELATION: Annotated[float, Field(strict=True, ge=0, lt=1)]


class BookOut(BaseModel):
    ISBN: str
    TITLE: str
    PUBLICATION_YEAR: int
    PUBLISHER: str


class RatingOut(BaseModel):
    ID: int
    USER_ID: int
    ISBN: str
    RATING: int


class RatingIn(BaseModel):
    RATING: Annotated[int, Field(strinct=True, ge=1, le=10)]


class User(BaseModel):
    user_id: str
    email: Union[str, None] = None

class UserMe(BaseModel):
    user_id: int


class UserInDB(User):
    hashed_password: str


class UserRegistration(BaseModel):
    EMAIL: EmailStr
    PASSWORD: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None