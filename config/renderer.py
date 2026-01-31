from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


async def custom_request_validation_exception_handler(request, exc):
    error_message = "Validation Error!"
    error_detail = exc.errors()

    if isinstance(error_detail, list):
        error_key = []
        for error in error_detail:
            if error.get('loc') and f"{error.get('loc')[-1]}" not in error_key:
                error_key.append(f"{error.get('loc')[-1]}")
                error_message += f" '{error.get('loc')[-1]}' {error.get('msg')} !"
    response_data = {"success": False, "message": error_message, "detail": jsonable_encoder(error_detail), 'data': None}
    return JSONResponse(content=jsonable_encoder(response_data), status_code=400)


async def custom_validation_error_handler(request, exc):
    error_message = "Validation Error!"
    errors = exc.errors()
    if not errors:
        error_detail = "Something went wrong"
        data = None
    else:
        err = errors[0]
        if err.get("ctx"):
            error_detail = err.get("ctx", {}).get("error", err.get("msg", "Something went wrong"))
        else:
            error_detail = err.get("msg", "Something went wrong")
        data = err
    response_data = {"success": False, "message": error_message, "detail": str(error_detail), "data": data}
    return JSONResponse(content=jsonable_encoder(response_data), status_code=400)


async def custom_http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )
