from domain_account.business.ports import UpdateCpfInputPort, UpdateCpfOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class UpdateCpfUseCase(UseCase[UpdateCpfInputPort, UpdateCpfOutputPort, AccountService]):
    """Use case for updating user CPF.

    This use case handles the updating of user CPF. It receives input data via an UpdateCpfInputPort,
    updates the CPF via the provided AccountService, and returns an UpdateCpfOutputPort indicating
    the success of the CPF update process.

    Args:
        service (AccountService): An instance of AccountService providing business logic for account-related operations.

    """

    def __init__(self, service: AccountService) -> None:
        """Initialize the UpdateCpfUseCase with the provided AccountService."""
        self.__account_repo = service

    async def __call__(self, input_port: UpdateCpfInputPort) -> UpdateCpfOutputPort:
        """Execute the update CPF use case.

        Updates the user CPF with the provided information via the AccountService.

        Args:
            input_port (UpdateCpfInputPort): The input port containing user UID and CPF.

        Returns:
            UpdateCpfOutputPort: An output port containing a message indicating the success of the CPF update process.

        """  # noqa: E501
        await self.__account_repo.update_cpf(input_port)
        return UpdateCpfOutputPort(msg="ok")
