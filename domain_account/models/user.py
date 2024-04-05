from pydantic import BaseModel, Field

from .address import Address


class User(BaseModel):
    """Model that defines user"""

    cpf: str = Field(examples=["77777777777"])
    address: Address
