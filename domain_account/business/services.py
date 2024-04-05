from abc import ABCMeta, abstractmethod

from .interfaces import Service
from .ports import RegisterInputPort


class AccountService(Service, metaclass=ABCMeta):
    """A service to give access to database client features."""

    @abstractmethod
    async def register(self, port: RegisterInputPort) -> None:
        """Register a new user"""
