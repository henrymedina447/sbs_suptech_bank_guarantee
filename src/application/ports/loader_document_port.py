from abc import ABC, abstractmethod
from typing import Any
from application.contracts.parameter_contract import ParameterContract
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity
from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository
from domain.repositories.internal_tables_repository import InternalTablesRepository
from domain.repositories.regulatory_report_repository import RegulatoryReportRepository


class LoaderDocumentPort(ABC):
    def __init__(self,
                 bk_g_m_r: BankGuaranteeMetadataRepository,
                 it_r: InternalTablesRepository,
                 rr_r: RegulatoryReportRepository
                 ):
        self._bk_g_m_r = bk_g_m_r
        self._it_r = it_r
        self._rr_r = rr_r

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
    def save_analysis(self, analysis_result: dict[str, Any]) -> None:
        ...
