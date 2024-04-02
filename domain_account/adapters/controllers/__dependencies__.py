from abc import ABCMeta
from typing import Any

from domain_account.business.__factory__ import BusinessFactory
from domain_account.business.account.use_case.login_use_case import LoginUseCase
from domain_account.business.account.use_case.register_use_case import RegisterUseCase


def bind_controller_dependencies(business_factory: BusinessFactory) -> None:
    _ControllerDependencyManager(business_factory)


class ControllerDependencyManagerIsNotInitializedException(RuntimeError):
    """Raised when the Controller Dependency Manager is used but has not been initialized"""

    def __init__(self) -> None:
        self.type = "Dependency Manager"
        self.msg = "Something is trying to use the ControllerDependencyManager without initialize it"
        super().__init__(self.msg)


class _Singleton(type):
    """Singleton pattern created to be used by ControllerDependencyManager"""

    _instances: dict[type, object] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class _ControllerDependencyManager(metaclass=_Singleton):
    """Responsible for retrieve the Use Cases already instantiated to the Controllers"""

    def __init__(self, business_factory: BusinessFactory | None = None) -> None:
        if business_factory:
            self.__factory = business_factory

    def register_use_case(self) -> RegisterUseCase:
        if self.__factory:
            return self.__factory.register_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()

    def login_use_case(self) -> LoginUseCase:
        if self.__factory:
            return self.__factory.login_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()


class _ControllerDependency(metaclass=ABCMeta):
    """Base class which emulates the Dependency Injection of FastAPI"""

    def __init__(self) -> None:
        self._dependency_manager = _ControllerDependencyManager()


class RegisterUseCaseDependency(_ControllerDependency):
    """Brings the Register Use Case to the Register Controller through the Fast API 'Depends'"""

    def __init__(self) -> None:
        super().__init__()
        self.execute = self._dependency_manager.register_use_case()


class LoginUseCaseDependency(_ControllerDependency):
    """Brings the Login Use Case to the Login Controller through the Fast API 'Depends'"""

    def __init__(self) -> None:
        super().__init__()
        self.execute = self._dependency_manager.login_use_case()
