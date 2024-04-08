import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from domain_account.adapters.controllers.__dependencies__ import (
    RegisterControllerDependencies,
    RetrieveUserControllerDependencies,
    UpdateAddressControllerDependencies,
)
from domain_account.business.ports import RegisterInputPort, RetrieveUserInputPort, UpdateAddressInputPort

from .dtos import (
    RegisterAccountInputDTO,
    RegisterAccountOutputDTO,
    RetrieveUserOutputDTO,
    UpdateAddressInputDTO,
    UpdateAddressOutputDTO,
)

account_controller = APIRouter()


@account_controller.post(
    "/register-account",
    response_model=RegisterAccountOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
async def register_account(
    dto: RegisterAccountInputDTO,
    dependencies: Annotated[RegisterControllerDependencies, Depends()],
) -> JSONResponse | RegisterAccountOutputDTO:
    """Register a new account.

    Args:
        dto (RegisterAccountInputDTO): The input DTO containing account information.
        dependencies (RegisterControllerDependencies): Dependencies for registering the account.

    Returns:
        JSONResponse | RegisterAccountOutputDTO: Response containing account registration details.

    """
    try:
        input_port = RegisterInputPort(**dto.model_dump(), uid=dependencies.uid)
        output_port = await dependencies.register_use_case(input_port)
        return RegisterAccountOutputDTO(msg=output_port.msg)
    except ValidationError as errors:
        output_errors = {}
        for error in errors.errors():
            output_errors[error["type"]] = error["msg"]
            logging.info(f"Warning [Register Account] | {error['type']} - {error['msg']}")
        content = {"msg": "error", "errors": output_errors}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@account_controller.get(
    "/retrieve-user",
    response_model=RetrieveUserOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def retrieve_user(
    dependencies: Annotated[RetrieveUserControllerDependencies, Depends()],
) -> JSONResponse | RetrieveUserOutputDTO:
    """Retrieve user registration information.

    Args:
        dependencies (RetrieveUserControllerDependencies): Dependencies for retrieving user information.

    Returns:
        JSONResponse | RetrieveUserOutputDTO: Response containing user registration details.

    """
    try:
        input_port = RetrieveUserInputPort(uid=dependencies.uid)
        output_port = await dependencies.retrieve_user_use_case(input_port)
        return RetrieveUserOutputDTO(**output_port.model_dump())
    except ValidationError as errors:
        output_errors = {}
        for error in errors.errors():
            output_errors[error["type"]] = error["msg"]
            logging.info(f"Warning [Retrieve User] | {error['type']} - {error['msg']}")
        content = {"msg": "error", "errors": output_errors}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


@account_controller.patch(
    "/update-address",
    response_model=UpdateAddressOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def update_address(
    dto: UpdateAddressInputDTO,
    dependencies: Annotated[UpdateAddressControllerDependencies, Depends()],
) -> JSONResponse | UpdateAddressOutputDTO:
    """Update user address.

    Args:
        dto (UpdateAddressInputDTO): The input DTO containing updated address information.
        dependencies (UpdateAddressControllerDependencies): Dependencies for updating user address.

    Returns:
        JSONResponse | UpdateAddressOutputDTO: Response containing updated user address details.

    """
    try:
        input_port = UpdateAddressInputPort(**dto.model_dump(), uid=dependencies.uid)
        output_port = await dependencies.update_address_use_case(input_port)
        return UpdateAddressOutputDTO(**output_port.model_dump())
    except ValidationError as errors:
        output_errors = {}
        for error in errors.errors():
            output_errors[error["type"]] = error["msg"]
            logging.info(f"Warning [Update Address] | {error['type']} - {error['msg']}")
        content = {"msg": "error", "errors": output_errors}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)
