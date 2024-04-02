from typing import TypedDict

from domain_account.adapters.__factory__ import FrameworksFactoryInterface

from .mongodb import MotorManager


class FrameworksConfig(TypedDict):
    """Specification of the configurations required by the Frameworks."""

    database_name: str
    database_uri: str
    service_name: str


class FrameworksFactory(FrameworksFactoryInterface[MotorManager]):
    """Responsible for instantiating the Frameworks classes with their linked dependencies.

    This class is responsible for creating instances of framework classes with their required dependencies,
    particularly for interacting with MongoDB using Motor.

    Args:
        config (FrameworksConfig): A dictionary containing configuration parameters for the framework.

    """

    def __init__(self, config: FrameworksConfig) -> None:
        """Initialize the FrameworksFactory with the provided configuration.

        Args:
            config (FrameworksConfig): A dictionary containing configuration parameters for the framework.

        """
        self.__config = config
        self.__manager = MotorManager(
            database_name=self.__config["database_name"],
            database_uri=self.__config["database_uri"],
            service_name=self.__config["service_name"],
        )

    async def connect(self) -> None:
        """Connect to the MongoDB database asynchronously."""
        await self.__manager.connect()

    def close(self) -> None:
        """Close the connection to the MongoDB database."""
        self.__manager.close()

    def database_framework(self) -> MotorManager:
        """Get the MotorManager instance representing the MongoDB database framework.

        Returns:
            MotorManager: An instance of MotorManager representing the MongoDB database framework.

        """
        return self.__manager
