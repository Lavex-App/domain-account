from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from fastapi import FastAPI

from domain_account.adapters.controllers.__binding__ import Binding
from domain_account.adapters.interfaces.document_database_service import DocumentDatabaseService
from domain_account.adapters.repositories.account_repository import AccountRepository
from domain_account.business.__factory__ import AdaptersFactoryInterface

T_provider_co = TypeVar("T_provider_co", bound=DocumentDatabaseService, covariant=True)


class FrameworksFactoryInterface(Generic[T_provider_co], metaclass=ABCMeta):
    """Interface for the Frameworks Factory according to the Adapters layer needs.

    This interface defines the contract for a factory that provides framework-related services,
    such as database access, to the adapters layer.

    """

    @abstractmethod
    def database_framework(self) -> DocumentDatabaseService:
        """Abstract method to retrieve the database framework instance."""


class AdaptersFactory(AdaptersFactoryInterface[AccountRepository]):
    """Responsible for instantiating the Adapters classes with their linked dependencies.

    This class is responsible for creating instances of adapter classes with their required dependencies,
    particularly for the account-related functionalities.

    Args:
        frameworks_factory (FrameworksFactoryInterface): An instance of a factory implementing the
            `FrameworksFactoryInterface`, providing access to the necessary frameworks.

    """

    def __init__(self, frameworks_factory: FrameworksFactoryInterface) -> None:
        """Initialize the AdaptersFactory with the provided frameworks factory.

        Args:
            frameworks_factory (FrameworksFactoryInterface): An instance of a factory implementing the
                `FrameworksFactoryInterface`.

        """
        self.__factory = frameworks_factory

    def account_service(self) -> AccountRepository:
        """Instantiate and return an AccountRepository with the configured database framework.

        Returns:
            AccountRepository: An instance of AccountRepository with the configured database framework.

        """
        return AccountRepository(self.__factory.database_framework())

    def register_routes(self, app: FastAPI) -> None:
        """Register routes for all controllers in the application.

        This method registers routes for all controllers in the application using the provided FastAPI instance.

        Args:
            app (FastAPI): The FastAPI instance to which routes will be registered.

        """
        Binding().register_all(app)
