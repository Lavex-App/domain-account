from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from domain_account.business.interfaces import InputPort, OutputPort, Service

T_input = TypeVar("T_input", bound=InputPort)
T_output = TypeVar("T_output", bound=OutputPort, covariant=True)
T_service = TypeVar("T_service", bound=Service)


class UseCase(Generic[T_input, T_output, T_service], metaclass=ABCMeta):
    """Class that execute a business rule"""

    @abstractmethod
    def __init__(self, service: T_service) -> None: ...

    @abstractmethod
    async def __call__(self, input_port: T_input) -> T_output: ...
