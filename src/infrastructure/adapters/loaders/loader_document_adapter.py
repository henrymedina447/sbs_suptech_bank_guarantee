import inspect
from typing import Any
from uuid import UUID

from pydantic_core import ValidationError

from application.contracts.parameter_contract import ParameterContract
from application.exceptions.collect_data_exception import CollectDataException
from application.ports.loader_document_port import LoaderDocumentPort
from application.states.analyze_data.analyse_data_state import AnalyzeDataState
from domain.enums.collect_data_errors_enum import CollectDataErrorsEnum
from domain.models.entities.analysis_result_report_entity import AnalysisResultReportEntity
from domain.models.entities.bank_guarantee_metadata_by_id_entity import BankGuaranteeMetadataByIdEntity
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity, MetadataEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity
from domain.repositories.analysis_result_report_repository import AnalysisResultReportRepository
from domain.repositories.analysis_result_report_status_repository import AnalysisResultReportStatusRepository
from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository
from domain.repositories.internal_tables_repository import InternalTablesRepository
from domain.repositories.regulatory_report_repository import RegulatoryReportRepository


class LoaderDocumentAdapter(LoaderDocumentPort):

    def __init__(self,
                 bk_g_m_r: BankGuaranteeMetadataRepository,
                 it_r: InternalTablesRepository,
                 rr_r: RegulatoryReportRepository,
                 ar_r: AnalysisResultReportRepository,
                 ar_s: AnalysisResultReportStatusRepository
                 ):
        super().__init__(bk_g_m_r, it_r, rr_r, ar_r, ar_s)

    def load_regulatory_report(self, parameters: ParameterContract) -> list[RegulatoryReportEntity]:
        try:
            results: list[dict[str, Any]] = self._rr_r.get_collection(
                user_id=parameters.legal_name,
                year=str(parameters.period_year),
                month=str(parameters.period_month),
            )
            rr_tables: list[RegulatoryReportEntity] = [RegulatoryReportEntity(**r) for r in results]
            return rr_tables
        except ValidationError as e:
            method_name = inspect.currentframe().f_code.co_name
            raise CollectDataException(
                reason=CollectDataErrorsEnum.u_regulatory_report,
                message=f"Al intentar una transformación en {method_name} "
            ) from e
        except CollectDataException as e:
            raise

    def load_internal_tables(self, parameters: ParameterContract) -> list[InternalTablesEntity]:
        try:
            results: list[dict[str, Any]] = self._it_r.get_collection(
                user_id=parameters.legal_name,
                year=str(parameters.period_year),
                month=str(parameters.period_month),
            )
            internal_tables: list[InternalTablesEntity] = [InternalTablesEntity(**r) for r in results]
            return internal_tables
        except ValidationError as e:
            method_name = inspect.currentframe().f_code.co_name
            raise CollectDataException(
                reason=CollectDataErrorsEnum.u_internal_table,
                message=f"Al intentar una transformación en {method_name} "
            ) from e
        except CollectDataException as e:
            raise

    def load_bank_guarantee_metadata(self, parameters: ParameterContract) -> list[BankGuaranteeEntity]:
        #return self._load_bank_guarantee_metadata_by_period(parameters)
        return self._load_bank_guarantee_metadata_by_ids(parameters)

    def save_analysis(self, source: UUID, analysis_result: AnalyzeDataState) -> tuple[bool, str | None]:
        try:
            key: str = self._ar_r.save_report(source, analysis_result)
            return True, key
        except Exception as e:
            print(f"error: {e}")
            return False, None

    def save_status(self, status: AnalysisResultReportEntity) -> None:
        self._ar_s.save_status(status)

    def _load_bank_guarantee_metadata_by_ids(self, parameters: ParameterContract) -> list[BankGuaranteeEntity]:
        response: list[dict[str, Any]] = self._bk_g_m_r.get_collection_by_ids(ids=parameters.bank_guarantees)
        print("response",response)
        try:
            response: list[dict[str, Any]] = self._bk_g_m_r.get_collection_by_ids(ids=parameters.bank_guarantees)
            aux_list: list[BankGuaranteeMetadataByIdEntity] = [BankGuaranteeMetadataByIdEntity.model_validate(r) for r
                                                               in response if
                                                               r.get("metadata", {}).get("period_year") is not None]
            return [self._normalize_to_bank_guarantee(r) for r in aux_list]

        except ValidationError as e:
            method_name = inspect.currentframe().f_code.co_name
            raise CollectDataException(
                reason=CollectDataErrorsEnum.u_bank_guarantee_metadata_table,
                message=f"Al intentar una transformación en {method_name} "
            ) from e
        except CollectDataException as e:
            raise

    def _load_bank_guarantee_metadata_by_period(self, parameters: ParameterContract) -> list[BankGuaranteeEntity]:
        try:
            results: list[dict[str, Any]] = self._bk_g_m_r.get_collection_by_period(
                user_id=parameters.legal_name,
                year=str(parameters.period_year),
                month=str(parameters.period_month)
            )
            metadata_tables = [BankGuaranteeEntity(**r) for r in results]
            return metadata_tables
        except ValidationError as e:
            method_name = inspect.currentframe().f_code.co_name
            raise CollectDataException(
                reason=CollectDataErrorsEnum.u_bank_guarantee_metadata_table,
                message=f"Al intentar una transformación en {method_name} "
            ) from e
        except CollectDataException as e:
            raise

    def _normalize_to_bank_guarantee(self, raw: BankGuaranteeMetadataByIdEntity) -> BankGuaranteeEntity:
        return BankGuaranteeEntity(
            file_name=raw.metadata.file_name,
            period_month=raw.metadata.period_month,
            period_year=raw.metadata.period_year,
            supervisory_record_id=raw.supervisory_record_id,
            type_document="carta fianza",
            metadata=MetadataEntity(
                letter_date=raw.metadata.letter_date,
                disbursed_amount=raw.metadata.disbursed_amount,
                reduced_amount=raw.metadata.reduced_amount,
                total_amount=raw.metadata.total_amount,
                letter_text=raw.metadata.letter_text,
                project_text=raw.metadata.project_text,
                promotor=raw.metadata.promotor
            )

        )
