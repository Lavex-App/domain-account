import logging
import certifi

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from domain_account.adapters.interfaces import DocumentDatabaseService


class MotorManager(DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]):
    """Manager for Motor (Async MongoDB Client).

    This class manages connections to a MongoDB database using the Motor asynchronous client.

    Args:
        service_name (str): The name of the service using the MotorManager.
        database_name (str): The name of the MongoDB database.
        database_uri (str): The URI of the MongoDB instance.

    Attributes:
        _logger (Logger): An instance of the logger for logging messages.
        _service_name (str): The name of the service using the MotorManager.
        _database_name (str): The name of the MongoDB database.
        _database_uri (str): The URI of the MongoDB instance.
        _client (AsyncIOMotorClient | None): The Motor asynchronous client instance.

    """

    def __init__(self, service_name: str, database_name: str, database_uri: str) -> None:
        """Initialize the MotorManager with the provided parameters."""
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self._service_name = service_name
        self._database_name = database_name
        self._database_uri = database_uri
        self._client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        """Connect to a MongoDB cluster asynchronously.

        Raises:
            ConnectionFailure: If a connection to the MongoDB cluster cannot be established.

        """
        self.close()
        try:
            ca = certifi.where()
            self._client = AsyncIOMotorClient(self._database_uri, appname=self._service_name, tlsCAFile=ca)
            await self._client.admin.command("ping")
        except ConnectionFailure:  # pragma: no cover
            self._logger.info("Server [%s] not available!", self._database_uri)
        else:
            self._logger.info("Connected to MongoDB [%s].", self._database_name)

    def close(self) -> None:
        """Close the current database connection."""
        if self._client is None:
            return
        self._client.close()
        self._logger.info("Closed MongoDB connection.")

    @property
    def client(self) -> AsyncIOMotorClient:
        """Return the instantiated MongoDB client.

        Returns:
            AsyncIOMotorClient: The instantiated MongoDB client.

        Raises:
            ValueError: If there is no MongoDB client instantiated.

        """
        if self._client is None:
            raise ValueError("There is no MongoDB client.")
        return self._client

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Return the current instance of a Database client based on the provided database name.

        Returns:
            AsyncIOMotorDatabase: The current instance of a Database client.

        """
        return self.client[self._database_name]
