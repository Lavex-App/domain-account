from passlib.context import CryptContext

from domain_account.business.account.use_case.exceptions import InvalidUserDataException
from domain_account.business.ports import LoginInputPort, LoginOutputPort
from domain_account.business.services import AccountService

from .interfaces import UseCase


class LoginUseCase(UseCase[LoginInputPort, LoginOutputPort, AccountService]):
    """Use case for user login.

    This use case handles the login process for users. It receives input data via a LoginInputPort,
    retrieves the user from the provided AccountService based on the provided phone number,
    verifies the provided password against the hashed password stored in the user data,
    and returns a LoginOutputPort indicating the success of the login process.

    Args:
        service (AccountService): An instance of AccountService providing business logic for account-related operations.

    """

    def __init__(self, service: AccountService) -> None:
        """Initialize the LoginUseCase with the provided AccountService."""
        self.__account_repo = service

    async def __call__(self, input_port: LoginInputPort) -> LoginOutputPort:
        """Execute the login use case.

        Retrieves the user based on the provided phone number,
        verifies the provided password against the hashed password stored in the user data,
        and returns a LoginOutputPort indicating the success of the login process.

        Args:
            input_port (LoginInputPort): The input port containing user login information.

        Returns:
            LoginOutputPort: An output port containing a message indicating the success of the login process.

        Raises:
            InvalidUserDataException: If either the user phone or password is incorrect.

        """
        user = await self.__account_repo.find_by_phone(input_port.phone)
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        if pwd_context.verify(input_port.hashed_password, user.hashed_password):
            return LoginOutputPort(msg="ok")
        raise InvalidUserDataException("Either User phone or password is wrong")
