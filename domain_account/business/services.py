from abc import ABCMeta, abstractmethod

from domain_account.models import User

from .interfaces import Service
from .ports import RegisterInputPort, RetrieveUserInputPort


class AccountService(Service, metaclass=ABCMeta):
    """
    A service providing access to features outside Business Layer.

    Methods:
        register(port): Register a new user.
        get_user(port): Retrieve user information.

    """

    @abstractmethod
    async def register(self, port: RegisterInputPort) -> None:
        """
        Register a new user.

        Args:
            port (RegisterInputPort): The input port containing user account information.
        """

    @abstractmethod
    async def get_user(self, port: RetrieveUserInputPort) -> User:
        """
        Retrieve user information.

        Args:
            port (RetrieveUserInputPort): The input port containing the user UID.

        Returns:
            User: An instance of the User model containing user information.
        """
