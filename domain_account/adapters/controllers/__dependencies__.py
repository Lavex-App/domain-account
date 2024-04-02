from abc import ABCMeta
from typing import Any, Self

from domain_account.business.__factory__ import BusinessFactory
from domain_account.business.account.use_case.login_use_case import LoginUseCase
from domain_account.business.account.use_case.register_use_case import RegisterUseCase


def bind_controller_dependencies(business_factory: BusinessFactory) -> None:
    _ControllerDependencyManager(business_factory)


class _Singleton(type):
    _instances = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _ControllerDependencyManager(metaclass=_Singleton):
    def __init__(self, business_factory: BusinessFactory | None = None) -> None:
        if business_factory:
            self.__factory = business_factory

    def register_use_case(self) -> RegisterUseCase:
        if self.__factory:
            return self.__factory.register_use_case()
        raise Exception("Controller Dependencies isn't initialized yet")

    def login_use_case(self) -> LoginUseCase:
        if self.__factory:
            return self.__factory.login_use_case()
        raise Exception("Controller Dependencies isn't initialized yet")


class _ControllerDependency(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._dependency_manager = _ControllerDependencyManager()


class RegisterUseCaseDependency(_ControllerDependency):
    def __init__(self) -> None:
        super().__init__()
        self.execute = self._dependency_manager.register_use_case()


class LoginUseCaseDependency(_ControllerDependency):
    def __init__(self) -> None:
        super().__init__()
        self.execute = self._dependency_manager.login_use_case()
