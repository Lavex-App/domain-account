from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from domain_account.business.account.use_case.register_use_case import RegisterUseCase

from .services import AccountService

T_account_service_co = TypeVar("T_account_service_co", bound=AccountService, covariant=True)


class AdaptersFactoryInterface(Generic[T_account_service_co], metaclass=ABCMeta):
    """Interface for the Adapters Factory according to the Business layer needs.

    This interface defines the contract for a factory that provides adapter services,
    such as account management, to the business layer.

    """

    @abstractmethod
    def account_service(self) -> T_account_service_co:
        """Abstract method to retrieve the account service instance."""


class BusinessFactory:
    """Responsible for instantiating the Business classes with their linked dependencies.

    This class is responsible for creating instances of business classes with their required dependencies,
    particularly for the account-related use cases.

    Args:
        adapters_factory (AdaptersFactoryInterface): An instance of a factory implementing the
            `AdaptersFactoryInterface`, providing access to the necessary adapter services.

    """

    def __init__(self, adapters_factory: AdaptersFactoryInterface) -> None:
        """Initialize the BusinessFactory with the provided adapters factory.

        Args:
            adapters_factory (AdaptersFactoryInterface): An instance of a factory implementing the
                `AdaptersFactoryInterface`.

        """
        self.__factory = adapters_factory

    def register_use_case(self) -> RegisterUseCase:
        """Instantiate and return a RegisterUseCase with the configured account service.

        Returns:
            RegisterUseCase: An instance of RegisterUseCase with the configured account service.

        """
        return RegisterUseCase(service=self.__factory.account_service())
