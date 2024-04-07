from domain_account.business.ports import RegisterInputPort, RegisterOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class RegisterUseCase(UseCase[RegisterInputPort, RegisterOutputPort, AccountService]):
    """Use case for user registration.

    This use case handles the registration of new users. It receives input data via a RegisterInputPort,
    registers the user via the provided AccountService, and returns a RegisterOutputPort indicating
    the success of the registration process.

    Args:
        service (AccountService): An instance of AccountService providing business logic for account-related operations.

    """

    def __init__(self, service: AccountService) -> None:
        """Initialize the RegisterUseCase with the provided AccountService."""
        self.__account_repo = service

    async def __call__(self, input_port: RegisterInputPort) -> RegisterOutputPort:
        """Execute the register use case.

        Registers a new user with the provided information via the AccountService.

        Args:
            input_port (RegisterInputPort): The input port containing user registration data.

        Returns:
            RegisterOutputPort: An output port containing a message indicating the success of the registration process.

        """
        await self.__account_repo.register(input_port)
        return RegisterOutputPort(msg="ok")
