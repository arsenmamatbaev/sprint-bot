from dataclasses import dataclass
from database import User


@dataclass
class PaymentLink:
    user: User
    payment_link: str

