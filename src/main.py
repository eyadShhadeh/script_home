from typing import Union
from fastapi import FastAPI
from src.controllers.user import user_route


def create_app() -> FastAPI:
    app = FastAPI(title='home_script')

    return app


app = create_app()


app.include_router(user_route, prefix="/user")


@app.get("/")
async def read_root():
    return "welcome to Home script for si-tech."
