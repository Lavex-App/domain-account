from abc import ABCMeta, abstractmethod

from domain_account.models import User

from .interfaces import Service
from .ports import RegisterInputPort, RetrieveUserInputPort, UpdateAddressInputPort, UpdateCpfInputPort


class AccountService(Service, metaclass=ABCMeta):
    """A service providing access to features outside Business Layer.

    Methods:
        register(port): Register a new user.
        get_user(port): Retrieve user information.
        update_address(port): Update user address.
        update_cpf(port): Update user CPF.

    """

    @abstractmethod
    async def register(self, port: RegisterInputPort) -> None:
        """Register a new user.

        Args:
            port (RegisterInputPort): The input port containing user account information.
        """

    @abstractmethod
    async def get_user(self, port: RetrieveUserInputPort) -> User:
        """Retrieve user information.

        Args:
            port (RetrieveUserInputPort): The input port containing the user UID.

        Returns:
            User: An instance of the User model containing user information.
        """

    @abstractmethod
    async def update_address(self, port: UpdateAddressInputPort) -> None:
        """Update user address.

        Args:
            port (UpdateAddressInputPort): The input port containing the user UID and updated address information.
        """

    @abstractmethod
    async def update_cpf(self, port: UpdateCpfInputPort) -> None:
        """Update user CPF.

        Args:
            port (UpdateCpfInputPort): The input port containing the user UID and updated CPF information.
        """
