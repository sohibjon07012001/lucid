import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
import config
from routes import admin_tools, auth, users, partners, ml_models
# import pandas as pd
app = FastAPI()


origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(admin_tools.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(partners.router)
app.include_router(ml_models.router)


register_tortoise(
    app,
    db_url=config.Database.CONNECTION_STRING,
    
    modules={
        'db': config.Database.MODULES
    },
    generate_schemas=True,
    add_exception_handlers=False
)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)