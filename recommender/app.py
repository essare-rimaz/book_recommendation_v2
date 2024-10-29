from fastapi import FastAPI

from database.db import engine

from database import models

import schemas as schemas
import book_rec as book_rec

from routers import users, public

models.Base.metadata.create_all(engine)

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **registration** and **login** logic is also here.",
    },
    {
        "name": "ratings",
        "description": "Manage ratings - some functionality is available for logged in users only.",
    },
    {
        "name": "recommendations",
        "description": "Our flagship functionality - figure out what to read next based on a book you already like.",
    },
    {
        "name": "books",
        "description": "Access detailed information about books in our database.",
    },
]

description = '''
Are you out of ideas what do read?

Your friends have a totally different taste when it comes to books?

All the recommendations you got never worked out?

Try our **recommendations** engine which could help you with all these problems.
You don't even have to register!
'''

app = FastAPI(
    title="Book Recommender",
    version="0.0.1",
    description=description,
    openapi_tags=tags_metadata
    )

app.include_router(users.router)
app.include_router(users.router, prefix="/v1")
app.include_router(users.router, prefix="/latest")
app.include_router(public.router)
app.include_router(public.router, prefix="/v1")
app.include_router(public.router, prefix="/latest")