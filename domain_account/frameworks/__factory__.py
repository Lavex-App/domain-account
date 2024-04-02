from typing import TypedDict

from domain_account.adapters.__factory__ import FrameworksFactoryInterface
from domain_account.adapters.interfaces.document_database_service import DocumentDatabaseService

from .mongodb import MotorManager


class FrameworksConfig(TypedDict):
    database_name: str
    database_uri: str
    service_name: str


class FrameworksFactory(FrameworksFactoryInterface[MotorManager]):
    def __init__(self, config: FrameworksConfig) -> None:
        self.__config = config
        self.__manager = MotorManager(
            database_name=self.__config["database_name"],
            database_uri=self.__config["database_uri"],
            service_name=self.__config["service_name"],
        )

    async def connect(self) -> None:
        await self.__manager.connect()

    def close(self) -> None:
        self.__manager.close()

    def database_framework(self) -> MotorManager:
        return self.__manager
