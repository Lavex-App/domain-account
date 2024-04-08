from domain_account.business.ports import UpdateAddressInputPort, UpdateAddressOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class UpdateAddressUseCase(UseCase[UpdateAddressInputPort, UpdateAddressOutputPort, AccountService]):
    """Use case for updating user address.

    This use case handles the updating of user address. It receives input data via an UpdateAddressInputPort,
    updates the address via the provided AccountService, and returns an UpdateAddressOutputPort indicating
    the success of the address update process.

    Args:
        service (AccountService): An instance of AccountService providing business logic for account-related operations.

    """

    def __init__(self, service: AccountService) -> None:
        """Initialize the UpdateAddressUseCase with the provided AccountService."""
        self.__account_repo = service

    async def __call__(self, input_port: UpdateAddressInputPort) -> UpdateAddressOutputPort:
        """Execute the update address use case.

        Updates the user address with the provided information via the AccountService.

        Args:
            input_port (UpdateAddressInputPort): The input port containing user address update data.

        Returns:
            UpdateAddressOutputPort: An output port containing a message indicating the success of the address update process.

        """  # noqa: E501
        await self.__account_repo.update_address(input_port)
        return UpdateAddressOutputPort(msg="ok")
