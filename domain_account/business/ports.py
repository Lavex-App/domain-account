from domain_account.models import Address, User

from .interfaces import InputPort, OutputPort


class RegisterInputPort(User, InputPort):
    """Input Port for register account"""

    uid: str


class RegisterOutputPort(OutputPort):
    """Output Port for register account"""

    msg: str


class UpdateAddressInputPort(Address, InputPort):
    """Input Port for update address"""

    uid: str


class UpdateAddressOutputPort(OutputPort):
    """Output Port for update address"""

    msg: str


class UpdateCpfInputPort(InputPort):
    """Input Port for update cpf"""

    uid: str
    cpf: str


class UpdateCpfOutputPort(OutputPort):
    """Output Port for update cpf"""

    msg: str


class RetrieveUserInputPort(InputPort):
    """Input Port for retrieve a registred user"""

    uid: str


class RetrieveUserOutputPort(User, OutputPort):
    """Output Port for retrieve a registred user"""

    msg: str
