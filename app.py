from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from typing_extensions import Annotated
from typing import List, Union

from passlib.context import CryptContext

import jwt
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone

from db import get_db, Book, Rating, User

from sqlalchemy import insert, exc
from sqlalchemy.orm import Session

import schemas
import book_rec

SECRET_KEY = "14ad83152e2c537778b24af53c187775fc26194d7b58210534c0f9fb166f7693"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#TODO on startup build tables

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(username: str, db: Session):
    user = db.query(User).filter(User.EMAIL==username).first()
    if user:
        return user

def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.PASSWORD_HASH):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    if current_user.DISABLED_BOOLEAN:
        raise HTTPException(status_code=400, detail="Test user")
    return current_user



@app.get("/recommendations/{isbn}", response_model=List[schemas.RecommendationOut], tags=["recommendations"])
def get_recommendations(isbn: str, db: Session = Depends(get_db)):
    corr_dataset = book_rec.get_ratings_of_related_books(isbn, db)
    correlations = book_rec.get_books_correlation(corr_dataset, isbn)
    averages = book_rec.get_books_average_rating(corr_dataset)
    recommendations = book_rec.get_final_dataset(correlations, averages, isbn, db)

    return recommendations


@app.get("/books/{isbn}", response_model=schemas.BookOut, tags=["books"])
def get_books(isbn: str, db: Session = Depends(get_db)):
    book_details = book_rec.get_book_details(isbn, db)

    return book_details


@app.get("/ratings/{isbn}", response_model=List[schemas.RatingOut], tags=["ratings"])
def get_ratings(isbn: str, db: Session = Depends(get_db)):
    ratings = book_rec.get_book_ratings(isbn, db)

    return ratings

@app.post("/ratings/{isbn}", status_code=status.HTTP_201_CREATED, tags=["ratings"])
def post_ratings(isbn: str, rating: schemas.RatingIn, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    new_rating = Rating(USER_ID = current_user.USER_ID, ISBN = isbn, RATING = rating.RATING)
    try:
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating
    except exc.DBAPIError as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=e.args)

@app.post("/token", status_code=status.HTTP_201_CREATED, tags=["auth"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    #if user.DISABLED_BOOLEAN:
    #    raise HTTPException(status_code=400, detail="Test user")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.EMAIL}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@app.get("/users/me", tags=["users"])
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return current_user

@app.post("/users/registration", status_code=status.HTTP_201_CREATED, tags=["users"])
async def users_register(
    user: schemas.UserRegistration,
    db: Session = Depends(get_db)
):
    new_user_email = user.EMAIL
    new_user_hashed_password = get_password_hash(user.PASSWORD)
    try:
        new_user = User(EMAIL=new_user_email, PASSWORD_HASH=new_user_hashed_password)
        db.add(new_user)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Something went wrong")


@app.get("users/ratings/", response_model=List[schemas.RatingOut], tags=["users"])
def get_ratings(isbn: str, current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    ratings = book_rec.get_book_ratings(current_user.USER, db)

    return ratings