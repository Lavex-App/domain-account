from domain_account.models import Address, User

from .interfaces import InputDTO, OutputDTO


class RegisterAccountInputDTO(User, InputDTO):
    """Input DTO for register account"""


class RegisterAccountOutputDTO(OutputDTO):
    """Output DTO for register account"""

    msg: str


class UpdateAddressInputDTO(Address, InputDTO):
    """Input DTO for update address"""


class UpdateAddressOutputDTO(OutputDTO):
    """Output DTO for update address"""

    msg: str


class RetrieveUserOutputDTO(User, OutputDTO):
    """Output DTO for retrieve an user"""
