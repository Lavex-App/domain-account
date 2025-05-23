from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from domain_account.business.use_case import (
    RegisterUseCase,
    RetrieveUserUseCase,
    UpdateAddressUseCase,
    UpdateCpfUseCase,
)

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
    """
    Responsible for instantiating the Business classes with their linked dependencies.

    This class is responsible for creating instances of business classes with their required dependencies,
    particularly for the account-related use cases.

    Args:
        adapters_factory (AdaptersFactoryInterface): An instance of a factory implementing the
            `AdaptersFactoryInterface`, providing access to the necessary adapter services.

    Methods:
        register_use_case(): Instantiate and return a RegisterUseCase with the configured account service.
        retrieve_user_use_case(): Instantiate and return a RetrieveUserUseCase with the configured account service.
        update_address_use_case(): Instantiate and return a UpdateAddressUseCase with the configured account service.
        update_cpf_use_case(): Instantiate and return a UpdateCpfUseCase with the configured account service.
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
        return RegisterUseCase(service=self.__account_service)

    def retrieve_user_use_case(self) -> RetrieveUserUseCase:
        """
        Instantiate and return a RetrieveUserUseCase with the configured account service.

        Returns:
            RetrieveUserUseCase: An instance of RetrieveUserUseCase with the configured account service.
        """
        return RetrieveUserUseCase(service=self.__account_service)

    def update_address_use_case(self) -> UpdateAddressUseCase:
        """
        Instantiate and return a UpdateAddressUseCase with the configured account service.

        Returns:
            UpdateAddressUseCase: An instance of UpdateAddressUseCase with the configured account service.
        """
        return UpdateAddressUseCase(service=self.__account_service)

    def update_cpf_use_case(self) -> UpdateCpfUseCase:
        """
        Instantiate and return a UpdateCpfUseCase with the configured account service.

        Returns:
            UpdateCpfUseCase: An instance of UpdateCpfUseCase with the configured account service.
        """
        return UpdateCpfUseCase(service=self.__account_service)

    @property
    def __account_service(self) -> AccountService:
        """
        Retrieve the account service instance.

        Returns:
            AccountService: An instance of the account service.
        """
        return self.__factory.account_service()
