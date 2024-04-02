from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from fastapi import FastAPI

from domain_account.adapters.controllers.__binding__ import Binding
from domain_account.adapters.interfaces.document_database_service import DocumentDatabaseService
from domain_account.adapters.repositories.account_repository import AccountRepository
from domain_account.business.__factory__ import AdaptersFactoryInterface
from domain_account.business.services import AccountService

T_provider = TypeVar("T_provider", bound=DocumentDatabaseService, covariant=True)


class FrameworksFactoryInterface(Generic[T_provider], metaclass=ABCMeta):
    @abstractmethod
    def database_framework(self) -> DocumentDatabaseService: ...


class AdaptersFactory(AdaptersFactoryInterface[AccountRepository]):
    def __init__(self, frameworks_factory: FrameworksFactoryInterface) -> None:
        self.__factory = frameworks_factory

    def account_service(self) -> AccountRepository:
        return AccountRepository(self.__factory.database_framework())

    def register_routes(self, app: FastAPI) -> None:
        Binding().register_all(app)
