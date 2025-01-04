from fastapi import FastAPI
# from .db import create_db_and_tables
from .routers import post, user, oauth2, vote 
from fastapi.middleware.cors import CORSMiddleware 
app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables() 


app.include_router(post.router)
app.include_router(user.router)
app.include_router(oauth2.router)
app.include_router(vote.router)
