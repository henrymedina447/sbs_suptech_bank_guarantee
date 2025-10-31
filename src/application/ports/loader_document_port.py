from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel

from application.contracts.parameter_contract import ParameterContract
from domain.models.entities.analysis_result_report_entity import AnalysisResultReportEntity
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity
from domain.repositories.analysis_result_report_repository import AnalysisResultReportRepository
from domain.repositories.analysis_result_report_status_repository import AnalysisResultReportStatusRepository
from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository
from domain.repositories.internal_tables_repository import InternalTablesRepository
from domain.repositories.regulatory_report_repository import RegulatoryReportRepository


class LoaderDocumentPort(ABC):
    def __init__(self,
                 bk_g_m_r: BankGuaranteeMetadataRepository,
                 it_r: InternalTablesRepository,
                 rr_r: RegulatoryReportRepository,
                 ar_r: AnalysisResultReportRepository,
                 ar_s: AnalysisResultReportStatusRepository
                 ):
        self._bk_g_m_r = bk_g_m_r
        self._it_r = it_r
        self._rr_r = rr_r
        self._ar_r = ar_r
        self._ar_s = ar_s

    @abstractmethod
    def load_regulatory_report(self, parameters: ParameterContract) -> list[RegulatoryReportEntity]:
        ...

    @abstractmethod
    def load_internal_tables(self, parameters: ParameterContract) -> list[InternalTablesEntity]:
        ...

    @abstractmethod
    def load_bank_guarantee_metadata(self, parameters: ParameterContract) -> list[BankGuaranteeEntity]:
        ...

    @abstractmethod
    def save_analysis(self, source: UUID, analysis_result: BaseModel) -> tuple[bool, str | None]:
        ...

    @abstractmethod
    def save_status(self, status:AnalysisResultReportEntity)->None:
        ...
