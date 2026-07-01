from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.schemas import (
    Customer,
    LoginRequest,
    TokenResponse
)

from app.services import (
    get_customers,
    authenticate_user
)

from app.auth import (
    create_access_token,
    verify_token
)

router = APIRouter()


# ---------------------------------
# LOGIN API
# ---------------------------------

@router.post(
    "/login",
    response_model=TokenResponse
)
def login(request: LoginRequest):

    user = authenticate_user(
        request.username,
        request.password
    )

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="Invalid Username or Password"
        )

    token = create_access_token(
        {
            "sub": user["username"],
            "role": user["role"]
        }
    )

    return {
        "access_token": token,
        "token_type": "Bearer"
    }


# ---------------------------------
# GET CUSTOMERS
# ---------------------------------

@router.get(
    "/customers",
    response_model=List[Customer]
)
def customers(
    payload: dict = Depends(verify_token)
):

    return get_customers()