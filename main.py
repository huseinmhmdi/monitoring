from fastapi import FastAPI
import uvicorn
from tortoise import Tortoise

import os
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import router
from config import TORTOISE_ORM



@asynccontextmanager
async def lifespan(app: FastAPI):
    # before start
    await Tortoise.init(config=TORTOISE_ORM)

    yield

    await Tortoise.close_connections()


app = FastAPI(
    debug=os.getenv("DEBUG"),
    root_path="/monitoring/v1",
    docs_url="/monitoring/docs",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
