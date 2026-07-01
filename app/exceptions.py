from fastapi import HTTPException


def internal_server_error(error):
    raise HTTPException(
        status_code=500,
        detail=str(error)
    )