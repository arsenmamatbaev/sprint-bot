from dataclasses import dataclass


@dataclass 
class User:
    user_id: int
    full_name: str
    username: str


@dataclass
class DataUser(User):
    payment_link: str
    level: str


@dataclass
class PaymentData:
    price1: int
    price2: int
    expire: int

