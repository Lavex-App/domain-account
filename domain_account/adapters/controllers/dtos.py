from domain_account.models import User

from .interfaces import InputDTO, OutputDTO


class RegisterAccountInputDTO(User, InputDTO):
    """Input DTO for register account"""


class RegisterAccountOutputDTO(OutputDTO):
    """Output DTO for register account"""

    msg: str
    errors: dict[str, str] | None = None
