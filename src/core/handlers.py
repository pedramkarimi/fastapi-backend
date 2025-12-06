# app/core/handlers.py

from typing import Any, Dict, List, Optional
import logging
from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from .exceptions import AppException

logger = logging.getLogger(__name__)


# ---------- مدل استاندارد خطا ----------

class ErrorResponse(BaseModel):
    message: str
    code: Optional[str] = None
    errors: Optional[List[Dict[str, Any]]] = None


# ---------- Pydantic Error Formatter (نسخه‌ی خودت) ----------

def format_pydantic_error(error: dict) -> dict:
    loc = ".".join(map(str, error.get("loc", [])[1:])) if error.get("loc") else ""
    err_type = error.get("type", "")
    msg = error.get("msg", "")
    ctx = error.get("ctx", {}) or {}

    result = {
        "field": loc,
        "error_type": err_type,
        "message": msg,
        "expected": ctx.get("expected"),
        "context": ctx,
    }

    # ---- انواع خطاهای Pydantic ----

    if err_type == "missing":
        result["message"] = "این فیلد اجباری است و ارسال نشده."
        return result

    if err_type.startswith("type_error") or "value is not a valid" in msg:
        expected_type = ctx.get("expected")
        result["message"] = f"نوع مقدار اشتباه است. نوع صحیح: {expected_type}"
        return result

    if err_type == "string_too_short":
        result["message"] = f"حداقل طول رشته: {ctx.get('min_length')}"
        return result

    if err_type == "string_too_long":
        result["message"] = f"حداکثر طول رشته: {ctx.get('max_length')}"
        return result

    if err_type == "list_too_short":
        result["message"] = f"حداقل آیتم‌های لیست: {ctx.get('min_items')}"
        return result

    if err_type == "list_too_long":
        result["message"] = f"حداکثر آیتم‌های لیست: {ctx.get('max_items')}"
        return result

    if err_type == "string_pattern_mismatch":
        result["message"] = f"فرمت رشته اشتباه است. الگو: {ctx.get('pattern')}"
        return result

    if err_type == "literal_error":
        result["message"] = f"باید یکی از مقادیر زیر باشد: {ctx.get('expected')}"
        return result

    if err_type == "greater_than":
        result["message"] = f"مقدار باید > {ctx.get('gt')} باشد"
        return result

    if err_type == "less_than":
        result["message"] = f"مقدار باید < {ctx.get('lt')} باشد"
        return result

    if err_type == "greater_than_equal":
        result["message"] = f"مقدار باید ≥ {ctx.get('ge')} باشد"
        return result

    if err_type == "less_than_equal":
        result["message"] = f"مقدار باید ≤ {ctx.get('le')} باشد"
        return result

    if err_type == "union":
        result["message"] = "مقدار با هیچ‌کدام از انواع union سازگار نیست."
        return result

    return result


# ---------- Exception Handlerها ----------

async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(
        "AppException on %s: code=%s message=%s extra=%s",
        request.url.path,
        exc.code,
        exc.message,
        exc.extra,
    )

    errors: Optional[List[Dict[str, Any]]] = None
    if exc.extra:
        # اگر extra دیکشنری بود، به صورت یک لیست برگردونیم
        if isinstance(exc.extra, list):
            errors = exc.extra
        else:
            errors = [exc.extra]

    error_response = ErrorResponse(
        message=exc.message,
        code=exc.code,
        errors=errors,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(
        "HTTPException on %s: status=%s detail=%r",
        request.url.path,
        exc.status_code,
        exc.detail,
    )

    # detail می‌تونه str یا dict باشه؛ ما حالت str رو استاندارد می‌کنیم
    if isinstance(exc.detail, str):
        message = exc.detail
        errors = None
    elif isinstance(exc.detail, dict):
        message = exc.detail.get("message", "HTTP error")
        errors = exc.detail.get("errors")
    else:
        message = "HTTP error"
        errors = None

    error_response = ErrorResponse(
        message=message,
        code=None,
        errors=errors,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = [format_pydantic_error(err) for err in exc.errors()]

    logger.info(
        "ValidationError on %s: %s",
        request.url.path,
        formatted_errors,
    )

    error_response = ErrorResponse(
        message="Validation failed. Check 'errors' for more info.",
        code="COMMON_VALIDATION_ERROR",
        errors=formatted_errors,
    )

    return JSONResponse(
        status_code=422,
        content=error_response.model_dump(),
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception on %s: %r",
        request.url.path,
        exc,
    )

    error_response = ErrorResponse(
        message="Internal server error",
        code="COMMON_SERVER_ERROR",
        errors=None,
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(),
    )
