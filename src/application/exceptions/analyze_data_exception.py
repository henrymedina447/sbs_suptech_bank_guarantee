from typing import Any

from domain.enums.analyze_data_errors_enum import AnalyzeDataErrorEnum


class AnalyzeDataException(Exception):
    """
    Contiene excepciones asociadas a la obtención del proceso de análisis
    """

    def __init__(self, reason: AnalyzeDataErrorEnum, message: str = "", raw_error: Any = None):
        self.reason = reason
        self.message = message
        self.raw_error = raw_error
        super().__init__(self.message)
