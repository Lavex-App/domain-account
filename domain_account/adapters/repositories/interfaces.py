from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from domain_account.adapters.interfaces.document_database_service import DocumentDatabaseService

T_provider = TypeVar("T_provider", bound=DocumentDatabaseService)


class Repository(Generic[T_provider], metaclass=ABCMeta):
    def __init__(self, provider: T_provider) -> None:
        self._provider = provider
