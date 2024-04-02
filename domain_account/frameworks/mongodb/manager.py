import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from domain_account.adapters.interfaces import DocumentDatabaseService


class MotorManager(DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]):
    """Manager for Motor (Async MongoDB Client)."""

    def __init__(self, service_name: str, database_name: str, database_uri: str):
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self._service_name = service_name
        self._database_name = database_name
        self._database_uri = database_uri
        self._client: AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        """Connect to a Mongodb cluster."""
        self.close()
        try:
            self._client = AsyncIOMotorClient(self._database_uri, appname=self._service_name)
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
        """Return the instantiated MongoDB client."""
        if self._client is None:
            raise ValueError("There is no MongoDB client.")
        return self._client

    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Return the current instance of a Database client."""
        return self.client[self._database_name]
