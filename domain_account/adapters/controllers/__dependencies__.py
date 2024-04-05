from abc import ABCMeta
from typing import Any

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from domain_account.adapters.interfaces.authentication_service import AuthenticationService, BearerToken
from domain_account.business.__factory__ import BusinessFactory
from domain_account.business.account.use_case.register_use_case import RegisterUseCase


def bind_controller_dependencies(
    business_factory: BusinessFactory, authentication_service: AuthenticationService
) -> None:
    _ControllerDependencyManager(business_factory, authentication_service)


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
    """Responsible for retrieve the Use Cases and Authentication service already instantiated to the Controllers"""

    def __init__(
        self,
        business_factory: BusinessFactory | None = None,
        authentication_service: AuthenticationService | None = None,
    ) -> None:
        if business_factory:
            self.__factory = business_factory
        if authentication_service:
            self.__auth = authentication_service

    def auth_service(self) -> AuthenticationService:
        if self.__auth:
            return self.__auth
        raise ControllerDependencyManagerIsNotInitializedException()

    def register_use_case(self) -> RegisterUseCase:
        if self.__factory:
            return self.__factory.register_use_case()
        raise ControllerDependencyManagerIsNotInitializedException()


class _ControllerDependency(metaclass=ABCMeta):
    """Base class which emulates the Dependency Injection of FastAPI"""

    def __init__(self, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> None:
        self._dependency_manager = _ControllerDependencyManager()
        auth = self._dependency_manager.auth_service()
        if credential is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Bearer authentication is needed",
                headers={"WWW-Authenticate": 'Bearer realm="auth_required"'},
            )
        bearer_token = BearerToken(credential.credentials)
        self.uid = auth.authenticate_by_token(bearer_token)


class RegisterControllerDependencies(_ControllerDependency):
    """Brings the Register Use Case to the Register Controller through the Fast API 'Depends'"""

    def __init__(self, credential: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))) -> None:
        super().__init__(credential)
        self.register_use_case = self._dependency_manager.register_use_case()
