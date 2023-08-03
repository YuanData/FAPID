from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    order_type: str = "Buy"
    symbol: str = "AUDCAD"
    volume: int = 1000


class Order(OrderBase):
    class Config:
        orm_mode = True


class Account(BaseModel):
    account: str
    email: str
    password: str


class ShowAccount(BaseModel):
    account: str

    class Config:
        orm_mode = True


class ShowOrder(BaseModel):
    id: int
    order_type: str
    symbol: str
    volume: int

    class Config:
        orm_mode = True


class Login(BaseModel):
    account: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    account: Optional[str] = None
