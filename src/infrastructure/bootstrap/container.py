from application.ports.loader_document_port import LoaderDocumentPort
from application.ports.messaging_status_port import MessagingStatusPort
from application.uses_cases.analyze_data_uc import AnalyzeDataUseCase
from application.uses_cases.collect_data_uc import CollectDataUseCase
from application.uses_cases.orchestrator_uc import OrchestratorWorkflow
from domain.repositories.analysis_result_report_repository import AnalysisResultReportRepository
from domain.repositories.analysis_result_report_status_repository import AnalysisResultReportStatusRepository
from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository
from domain.repositories.internal_tables_repository import InternalTablesRepository
from domain.repositories.regulatory_report_repository import RegulatoryReportRepository
from infrastructure.adapters.loaders.dynamo.dynamo_analysis_result_status_table_repository import \
    DynamoAnalysisResultStatusRepository
from infrastructure.adapters.loaders.dynamo.dynamo_bank_guarantee_metadata_repository import \
    DynamoBankGuaranteeMetadataRepository
from infrastructure.adapters.loaders.dynamo.dynamo_internal_tables_repository import DynamoInternalTablesRepository
from infrastructure.adapters.loaders.loader_document_adapter import LoaderDocumentAdapter
from infrastructure.adapters.loaders.dynamo.dynamo_regulatory_reports_repository import \
    DynamoRegulatoryReportsRepository
from infrastructure.adapters.loaders.s3.s3_analysis_result_report_repository import S3AnalysisResultReportRepository
from infrastructure.adapters.messaging.sqs_messaging_status_adapter import SqsMessagingStatusAdapter


def build_workflow() -> OrchestratorWorkflow:
    it_r: InternalTablesRepository = DynamoInternalTablesRepository()
    rr_r: RegulatoryReportRepository = DynamoRegulatoryReportsRepository()
    bk_g_m_r: BankGuaranteeMetadataRepository = DynamoBankGuaranteeMetadataRepository()
    ar_r: AnalysisResultReportRepository = S3AnalysisResultReportRepository()
    ar_s: AnalysisResultReportStatusRepository = DynamoAnalysisResultStatusRepository()

    loader_document: LoaderDocumentPort = LoaderDocumentAdapter(
        bk_g_m_r=bk_g_m_r,
        it_r=it_r,
        rr_r=rr_r,
        ar_r=ar_r,
        ar_s=ar_s
    )
    messaging:MessagingStatusPort=SqsMessagingStatusAdapter()
    analyze_data_uc: AnalyzeDataUseCase = AnalyzeDataUseCase()
    collect_data_uc: CollectDataUseCase = CollectDataUseCase(
        loader_document=loader_document,
    )
    workflow = OrchestratorWorkflow(
        collect_data_uc=collect_data_uc,
        analyze_data_uc=analyze_data_uc,
        loader_document=loader_document,
        messaging=messaging
    )
    return workflow
