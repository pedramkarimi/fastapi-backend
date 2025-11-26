from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []

    for error in exc.errors():
        formatted_errors.append(format_pydantic_error(error))

    return JSONResponse(
        status_code=422,
        content={
            "detail": formatted_errors,
            "message": "Validation failed. Check the 'detail' field for more info.",
        },
    )


def format_pydantic_error(error: dict):
    loc = ".".join(map(str, error.get("loc", [])[1:])) if error.get("loc") else ""
    err_type = error.get("type", "")
    msg = error.get("msg", "")
    ctx = error.get("ctx", {})

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
