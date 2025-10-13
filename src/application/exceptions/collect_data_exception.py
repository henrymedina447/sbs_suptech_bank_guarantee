from typing import Any
from domain.enums.collect_data_errors_enum import CollectDataErrorsEnum


class CollectDataException(Exception):
    """
    Contiene excepciones asociadas a la obtención de cualquier dato de las tablas dynamo
    """

    def __init__(self, reason: CollectDataErrorsEnum, message: str = "", raw_error: Any = None) -> None:
        self.reason = reason
        self.message = message
        self.raw_error = raw_error
        super().__init__(self.message)
