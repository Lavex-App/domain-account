from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from domain_account.adapters.interfaces.document_database_service import DocumentDatabaseService
from domain_account.business.ports import RegisterInputPort
from domain_account.business.services import AccountService

from .interfaces import Repository

ProviderType = DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]


class AccountRepository(
    Repository[DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]],
    AccountService,
):
    """A repository class responsible for interacting with a document database to manage user accounts.

    This class extends `Repository`, which defines the basic repository interface, and `AccountService`,
    which provides business logic for account-related operations.

    Args:
        provider (ProviderType): An instance of `DocumentDatabaseService` providing access to the document database.

    Attributes:
        _provider (ProviderType): The provider for accessing the document database.
        __users_collection: Collection in the document database where user records are stored.

    Methods:
        register(port): Registers a new user account in the database.

    """

    def __init__(self, provider: ProviderType) -> None:
        """Initialize the AccountRepository with a document database provider."""
        super().__init__(provider)
        self.__users_collection = self._provider.database["users"]

    async def register(self, port: RegisterInputPort) -> None:
        """Register a new user account in the database.

        Args:
            port (RegisterInputPort): The input port containing user account information.

        """
        await self.__users_collection.insert_one(port.model_dump())
