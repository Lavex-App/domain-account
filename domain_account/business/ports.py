from pydantic_extra_types.phone_numbers import PhoneNumber

from domain_account.models import User

from .interfaces import InputPort, OutputPort


class LoginInputPort(InputPort):
    """Input Port for login an user"""

    phone: PhoneNumber
    hashed_password: str


class LoginOutputPort(OutputPort):
    """Output Port for login an user"""

    msg: str


class RegisterInputPort(User, InputPort):
    """Input Port for register account"""


class RegisterOutputPort(OutputPort):
    """Output Port for register account"""

    msg: str
