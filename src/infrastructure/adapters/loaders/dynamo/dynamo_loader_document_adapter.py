from typing import Any
from application.contracts.parameter_contract import ParameterContract
from application.exceptions.collect_data_exception import CollectDataException
from application.ports.loader_document_port import LoaderDocumentPort
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity
from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository
from domain.repositories.internal_tables_repository import InternalTablesRepository
from domain.repositories.regulatory_report_repository import RegulatoryReportRepository


class DynamoLoaderDocumentAdapter(LoaderDocumentPort):

    def __init__(self,
                 bk_g_m_r: BankGuaranteeMetadataRepository,
                 it_r: InternalTablesRepository,
                 rr_r: RegulatoryReportRepository
                 ):
        super().__init__(bk_g_m_r, it_r, rr_r)

    def load_regulatory_report(self, parameters: ParameterContract) -> list[RegulatoryReportEntity]:
        pass

    def load_internal_tables(self, parameters: ParameterContract) -> list[InternalTablesEntity]:
        try:
            results: list[dict[str, Any]] = self._it_r.get_collection(
                user_id=parameters.legal_name,
                year=str(parameters.period_year),
                month=str(parameters.period_month),
            )
            internal_tables: list[InternalTablesEntity] = [InternalTablesEntity(**r) for r in results]
            return internal_tables
        except CollectDataException as e:
            print("error", e)
            return []

    def load_bank_guarantee_metadata(self, parameters: ParameterContract) -> list[BankGuaranteeEntity]:
        pass

    def save_analysis(self, analysis_result: dict[str, Any]) -> None:
        pass
