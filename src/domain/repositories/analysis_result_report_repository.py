from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel


class AnalysisResultReportRepository(ABC):

    @abstractmethod
    def save_report(self, source: UUID, report: BaseModel) -> str:
        """
        Guarda el reporte del análisis dentro del s3
        :param source:
        :param report:
        :return:
        """
        ...
