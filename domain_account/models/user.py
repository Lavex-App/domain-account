from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from .address import Address


class User(BaseModel):
    """Model that defines user"""

    full_name: str = Field(examples=["Vinicius Abade"])
    cpf: str = Field(examples=["77777777777"])
    email: EmailStr = Field(examples=["abade@lavex.com"])
    phone: PhoneNumber = Field(examples=["+5541977777777"])
    hashed_password: str = Field(examples=["61dbb982b063127a9abaac92b9eb394905e23ba50e36b6d8050bc9dc623ae308"])
    address: Address
