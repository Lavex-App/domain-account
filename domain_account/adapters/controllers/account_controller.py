import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from domain_account.adapters.controllers.__dependencies__ import LoginUseCaseDependency, RegisterUseCaseDependency
from domain_account.business.account.use_case.exceptions import InvalidUserDataException, UserNotFoundException
from domain_account.business.ports import LoginInputPort, RegisterInputPort

from .dtos import LoginInputDTO, LoginOutputDTO, RegisterAccountInputDTO, RegisterAccountOutputDTO

account_controller = APIRouter()


@account_controller.post(
    "/register-account",
    response_model=RegisterAccountOutputDTO,
    status_code=status.HTTP_201_CREATED,
)
async def register_account(
    dto: RegisterAccountInputDTO,
    use_case_dependency: Annotated[RegisterUseCaseDependency, Depends(RegisterUseCaseDependency)],
) -> JSONResponse | RegisterAccountOutputDTO:
    """Route for register account"""

    try:
        output_port = await use_case_dependency.execute(RegisterInputPort(**dto.model_dump()))
        return RegisterAccountOutputDTO(msg=output_port.msg)
    except ValidationError as errors:
        output_errors = {}
        for error in errors.errors():
            output_errors[error["type"]] = error["msg"]
            logging.info(f"Warning [Register Account] | {error['type']} - {error['msg']}")
        content = RegisterAccountOutputDTO(msg="error", errors=output_errors)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content.model_dump())


@account_controller.post(
    "/login",
    response_model=LoginOutputDTO,
    status_code=status.HTTP_200_OK,
)
async def login(
    dto: LoginInputDTO,
    use_case_dependency: Annotated[LoginUseCaseDependency, Depends(LoginUseCaseDependency)],
) -> JSONResponse | LoginOutputDTO:
    """Route for login an user"""

    try:
        output_port = await use_case_dependency.execute(LoginInputPort(**dto.model_dump()))
        return LoginOutputDTO(msg=output_port.msg)
    except ValidationError as errors:
        output_errors = {}
        for error in errors.errors():
            output_errors[error["type"]] = error["msg"]
            logging.info(f"Info [Login] | {error['type']} - {error['msg']}")
        content = LoginOutputDTO(msg="error", errors=output_errors)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content.model_dump())
    except UserNotFoundException as error:
        logging.info(f"Info [Login] | {error.type} - {error.msg}")
        content = LoginOutputDTO(msg="error", errors={"type": error.type, "msg": error.msg})
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=content.model_dump())
    except InvalidUserDataException as error:
        logging.info(f"Info [Login] | {error.type} - {error.msg}")
        content = LoginOutputDTO(msg="error", errors={"type": error.type, "msg": error.msg})
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content.model_dump())
