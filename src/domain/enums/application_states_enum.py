from enum import StrEnum


class ApplicationStatesEnum(StrEnum):
    processed = "letter-analysis.processed"
    error = "letter-analysis.processing-error"
