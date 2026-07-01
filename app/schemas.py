from pydantic import BaseModel


class Customer(BaseModel):
    CUSTOMER_ID: int
    CUSTOMER_NAME: str
    CITY: str
    EMAIL: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str