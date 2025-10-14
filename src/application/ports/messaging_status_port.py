from abc import ABC, abstractmethod

from domain.models.entities.analysis_result_report_entity import AnalysisResultReportEntity


class MessagingStatusPort(ABC):

    @abstractmethod
    def publish_status(self, status: AnalysisResultReportEntity) -> None:
        ...
