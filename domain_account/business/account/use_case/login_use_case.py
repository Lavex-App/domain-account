from passlib.context import CryptContext

from domain_account.business.account.use_case.exceptions import InvalidUserDataException
from domain_account.business.ports import LoginInputPort, LoginOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class LoginUseCase(UseCase[LoginInputPort, LoginOutputPort, AccountService]):
    """Use case for login an user"""

    def __init__(self, service: AccountService) -> None:
        self.__account_repo = service

    async def __call__(self, input_port: LoginInputPort) -> LoginOutputPort:
        user = await self.__account_repo.find_by_phone(input_port.phone)
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_context.verify(input_port.hashed_password, user.hashed_password):
            return LoginOutputPort(msg="ok")
        raise InvalidUserDataException("Either User phone or password is wrong")
