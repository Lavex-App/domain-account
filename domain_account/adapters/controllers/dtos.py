from pydantic import BaseModel
from pydantic_extra_types.phone_numbers import PhoneNumber

from domain_account.models import User

from .interfaces import InputDTO, OutputDTO


class RegisterAccountInputDTO(User, InputDTO):
    """Input DTO for register account"""


class RegisterAccountOutputDTO(OutputDTO):
    """Output DTO for register account"""

    msg: str
    errors: dict[str, str] | None = None


class LoginInputDTO(InputDTO):
    """Input DTO for login an user"""

    phone: PhoneNumber
    hashed_password: str


class LoginOutputDTO(OutputDTO):
    """Output DTO for login an user"""

    msg: str
    errors: dict[str, str] | None = None
