from fastapi import status
from fastapi.responses import JSONResponse

def custom_response(data: dict, status_code: int = status.HTTP_200_OK):
    return JSONResponse(content=data, status_code=status_code)
