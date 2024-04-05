from pydantic import BaseModel
from pydantic.fields import Field


class Address(BaseModel):
    """Model that defines address"""

    city: str = Field(examples=["Curitiba"])
    cep: str = Field(examples=["77777777"])
    street_name: str = Field(examples=["Rua Beltrano do Ciclano"])
    number: str = Field(examples=["777"])
    complement: str = Field(examples=["Apto 7"])
