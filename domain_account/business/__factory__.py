from abc import ABCMeta, abstractmethod
from typing import Generic

from typing_extensions import TypeVar

from domain_account.business.account.use_case.login_use_case import LoginUseCase
from domain_account.business.account.use_case.register_use_case import RegisterUseCase

from .services import AccountService

T_account_service = TypeVar("T_account_service", bound=AccountService, covariant=True)


class AdaptersFactoryInterface(Generic[T_account_service], metaclass=ABCMeta):
    @abstractmethod
    def account_service(self) -> T_account_service: ...


class BusinessFactory:
    def __init__(self, adapters_factory: AdaptersFactoryInterface) -> None:
        self.__factory = adapters_factory

    def register_use_case(self) -> RegisterUseCase:
        return RegisterUseCase(service=self.__factory.account_service())

    def login_use_case(self) -> LoginUseCase:
        return LoginUseCase(service=self.__factory.account_service())
