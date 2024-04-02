from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from domain_account.adapters.interfaces.document_database_service import DocumentDatabaseService
from domain_account.business.account.use_case.exceptions import UserNotFoundException
from domain_account.business.ports import RegisterInputPort, User
from domain_account.business.services import AccountService

from .interfaces import Repository

ProviderType = DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]


class AccountRepository(
    Repository[DocumentDatabaseService[AsyncIOMotorClient, AsyncIOMotorDatabase]],
    AccountService,
):
    def __init__(self, provider: ProviderType) -> None:
        super().__init__(provider)
        self.__users_collection = self._provider.database["users"]

    async def register(self, port: RegisterInputPort) -> None:
        await self.__users_collection.insert_one(port.model_dump())

    async def find_by_phone(self, phone: str) -> User:
        found_user: dict[str, Any] | None = await self.__users_collection.find_one({"phone": phone})
        if found_user:
            return User(**found_user)
        raise UserNotFoundException()
