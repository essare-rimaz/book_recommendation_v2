from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from typing_extensions import Annotated

import schemas as schemas

from sqlalchemy.orm import Session

from tools.auth import get_current_active_user, get_password_hash, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

from database.db import get_db
from database.models import User, Rating

from datetime import timedelta

from sqlalchemy import exc


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", tags=["users"])
def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    summary="Get your user profile details"
):
    return schemas.UserMe(user_id=current_user.USER_ID)


@router.post("/registration", status_code=status.HTTP_201_CREATED, tags=["users"])
def users_register(
    user: schemas.UserRegistration,
    db: Session = Depends(get_db),
    summary="Register in order to rate books and use other features"
):
    new_user_email = user.EMAIL
    new_user_hashed_password = get_password_hash(user.PASSWORD)
    try:
        new_user = User(EMAIL=new_user_email, PASSWORD_HASH=new_user_hashed_password)
        db.add(new_user)
        db.commit()
    except exc.DBAPIError as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=e.args)


@router.post("/ratings/{isbn}", status_code=status.HTTP_201_CREATED, tags=["ratings"])
def post_ratings(
    isbn: str, 
    rating: schemas.RatingIn, 
    current_user: Annotated[schemas.User, Depends(get_current_active_user)], 
    db: Session = Depends(get_db),
    summary="Give a book your rating - the higher the better"
):
    new_rating = Rating(USER_ID = current_user.USER_ID, ISBN = isbn, RATING = rating.RATING)
    try:
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return new_rating
    except exc.DBAPIError as e:
        db.rollback()
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=e.args)


@router.post("/token", status_code=status.HTTP_201_CREATED)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
    summary="Get your auth token"
) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.EMAIL}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")