from fastapi import FastAPI
from .logging import logging_middleware

def setup_middlewares(app: FastAPI):
    app.middleware("http")(logging_middleware)