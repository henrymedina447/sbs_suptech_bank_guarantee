from application.ports.loader_document_port import LoaderDocumentPort
from application.uses_cases.analyze_data_uc import AnalyzeDataUseCase
from application.uses_cases.collect_data_uc import CollectDataUseCase
from application.uses_cases.orchestrator_uc import OrchestratorWorkflow
from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository
from domain.repositories.internal_tables_repository import InternalTablesRepository
from domain.repositories.regulatory_report_repository import RegulatoryReportRepository
from infrastructure.adapters.loaders.dynamo.dynamo_bank_guarantee_metadata_repository import \
    DynamoBankGuaranteeMetadataRepository
from infrastructure.adapters.loaders.dynamo.dynamo_internal_tables_repository import DynamoInternalTablesRepository
from infrastructure.adapters.loaders.dynamo.dynamo_loader_document_adapter import DynamoLoaderDocumentAdapter
from infrastructure.adapters.loaders.dynamo.dynamo_regulatory_reports_repository import \
    DynamoRegulatoryReportsRepository


def build_workflow() -> OrchestratorWorkflow:
    it_r: InternalTablesRepository = DynamoInternalTablesRepository()
    rr_r: RegulatoryReportRepository = DynamoRegulatoryReportsRepository()
    bk_g_m_r: BankGuaranteeMetadataRepository = DynamoBankGuaranteeMetadataRepository()

    loader_document: LoaderDocumentPort = DynamoLoaderDocumentAdapter(
        bk_g_m_r=bk_g_m_r,
        it_r=it_r,
        rr_r=rr_r,
    )
    analyze_data_uc: AnalyzeDataUseCase = AnalyzeDataUseCase()
    collect_data_uc: CollectDataUseCase = CollectDataUseCase(
        loader_document=loader_document,
    )
    workflow = OrchestratorWorkflow(
        collect_data_uc=collect_data_uc,
        analyze_data_uc=analyze_data_uc,
        loader_document=loader_document,
    )
    return workflow
