from abc import ABC, abstractmethod
from pydantic import BaseModel


class AnalysisResultReportStatusRepository(ABC):

    @abstractmethod
    def save_status(self, result: BaseModel) -> None:
        """
        Cuando se guarda el reporte en el s3, el key autogenerado se envía al atabla dynamo de registro
        de salidas
        :param result:
        :return:
        """
        ...
