import logging
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from domain_account.adapters.controllers.__dependencies__ import RegisterControllerDependencies
from domain_account.business.ports import RegisterInputPort

from .dtos import RegisterAccountInputDTO, RegisterAccountOutputDTO

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
    """Route for register account"""
    try:
        input_port = RegisterInputPort(**dto.model_dump(), uid=dependencies.uid)
        output_port = await dependencies.register_use_case(input_port)
        return RegisterAccountOutputDTO(msg=output_port.msg)
    except ValidationError as errors:
        output_errors = {}
        for error in errors.errors():
            output_errors[error["type"]] = error["msg"]
            logging.info(f"Warning [Register Account] | {error['type']} - {error['msg']}")
        content = RegisterAccountOutputDTO(msg="error", errors=output_errors)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content.model_dump())
