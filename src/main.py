from fastapi import FastAPI, HTTPException
from .api.v1.router import router as api_v1_router
from fastapi.exceptions import RequestValidationError
from .core.exceptions import AppException
from .core.handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI(debug=True)
app.include_router(api_v1_router, prefix="/api/v1")
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(AppException, app_exception_handler)