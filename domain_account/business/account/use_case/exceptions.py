class BusinessException(RuntimeWarning):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.type = "Business"
        self.msg = msg


class MalformattedException(BusinessException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class InvalidUserDataException(BusinessException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class UserNotFoundException(BusinessException):
    def __init__(self) -> None:
        super().__init__("User not found")
