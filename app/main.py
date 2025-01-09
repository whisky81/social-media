from fastapi import FastAPI
# from .db import create_db_and_tables
from .routers import post, user, oauth2, vote 
from fastapi.middleware.cors import CORSMiddleware 


description = '''
    Social Media helps you do awesome stuff. 
    
    ## Users
    - You will be able to:
    * **Create account**: You must be have a account to use API
    * **Read user**: You can view the profiles of other users and yourself. 
    
    ## Posts 
    - You will be able to read, post, update and delete your own posts. 
    - You will be able to read and on other users' posts.
'''

app = FastAPI(
    title="Social Media",
    description=description,
    version="0.0.1",
    contact={
        "name": "roller",
        "email": "anhwhisky81@outlook.com"
    }
)


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
