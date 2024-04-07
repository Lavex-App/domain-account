from domain_account.business.ports import RetrieveUserInputPort, RetrieveUserOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class RetrieveUserUseCase(UseCase[RetrieveUserInputPort, RetrieveUserOutputPort, AccountService]):
    """Use case for retrieving user data.

    This use case retrieves user data from the account repository based on the provided UID.

    Args:
        service (AccountService): An instance of AccountService providing business logic for account-related operations.

    """

    def __init__(self, service: AccountService) -> None:
        """Initialize the RetrieveUserUseCase with the provided AccountService."""
        self.__service = service

    async def __call__(self, input_port: RetrieveUserInputPort) -> RetrieveUserOutputPort:
        """Execute the retrieve user use case.

        Retrieves user data from the account repository based on the provided UID.

        Args:
            input_port (RetrieveUserInputPort): The input port containing the UID of the user to retrieve.

        Returns:
            RetrieveUserOutputPort: An output port containing the retrieved user data.

        """
        user = await self.__service.get_user(input_port)
        return RetrieveUserOutputPort(**user.model_dump())
