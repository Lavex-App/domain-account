from domain_account.models import User

from .interfaces import InputPort, OutputPort


class RegisterInputPort(User, InputPort):
    """Input Port for register account"""

    uid: str


class RegisterOutputPort(OutputPort):
    """Output Port for register account"""

    msg: str
