from passlib.context import CryptContext

from domain_account.business.ports import RegisterInputPort, RegisterOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class RegisterUseCase(UseCase[RegisterInputPort, RegisterOutputPort, AccountService]):
    """Use case for user register"""

    def __init__(self, service: AccountService) -> None:
        self.__account_repo = service

    async def __call__(self, input_port: RegisterInputPort) -> RegisterOutputPort:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        input_port.hashed_password = pwd_context.hash(input_port.hashed_password)
        await self.__account_repo.register(input_port)
        return RegisterOutputPort(msg="ok")
