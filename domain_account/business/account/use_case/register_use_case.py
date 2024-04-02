from passlib.context import CryptContext

from domain_account.business.ports import RegisterInputPort, RegisterOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class RegisterUseCase(UseCase[RegisterInputPort, RegisterOutputPort, AccountService]):
    """Use case for user registration.

    This use case handles the registration of new users. It receives input data via a RegisterInputPort,
    hashes the user's password using bcrypt, registers the user via the provided AccountService, and returns
    a RegisterOutputPort indicating the success of the registration process.

    Args:
        service (AccountService): An instance of AccountService providing business logic for account-related operations.

    """

    def __init__(self, service: AccountService) -> None:
        """Initialize the RegisterUseCase with the provided AccountService."""
        self.__account_repo = service

    async def __call__(self, input_port: RegisterInputPort) -> RegisterOutputPort:
        """Execute the register use case.

        Hashes the user's password using bcrypt, registers the user via the provided AccountService,
        and returns a RegisterOutputPort indicating the success of the registration process.

        Args:
            input_port (RegisterInputPort): The input port containing user account information.

        Returns:
            RegisterOutputPort: An output port containing a message indicating the success of the registration process.

        """
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        input_port.hashed_password = pwd_context.hash(input_port.hashed_password)
        await self.__account_repo.register(input_port)
        return RegisterOutputPort(msg="ok")
