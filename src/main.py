from fastapi import FastAPI
from .api.v1.router import router as api_v1_router
from fastapi.exceptions import RequestValidationError
from .core.exceptions import validation_exception_handler

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(api_v1_router, prefix="/api/v1")