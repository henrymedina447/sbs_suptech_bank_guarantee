from uuid import UUID
import boto3
from botocore.config import Config

from application.states.analyze_data.analyse_data_state import AnalyzeDataState
from domain.repositories.analysis_result_report_repository import AnalysisResultReportRepository
from infrastructure.config.app_settings import get_app_settings, AwsSettings, AppSettings


class S3AnalysisResultReportRepository(AnalysisResultReportRepository):
    def __init__(self):
        self._app_setting:AppSettings = get_app_settings()
        base = self._app_setting.s3_settings.prefix.strip("/")
        self._bucket = self._app_setting.s3_settings.bucket
        self._base_prefix = f"{base}/" if base else ""

    def _key(self, source: UUID) -> str:
        return f"{self._base_prefix}{str(source)}.json"

    def _s3_client(self):
        _cfg = Config(
            retries={"max_attempts": 10, "mode": "standard"},
            connect_timeout=3,
            read_timeout=5
        )
        aws: AwsSettings = self._app_setting.aws_settings
        return boto3.client("s3", region_name=aws.region, config=_cfg)

    def save_report(self, source:UUID,report: AnalyzeDataState) -> str:
        source: UUID = source
        # Construimos la ruta en S3
        key = self._key(source)
        # Configuración del bucket
        body: bytes = report.model_dump_json().encode("utf-8")
        # Extras
        extra = {"ContentType": "application/json"}
        self._s3_client().put_object(Bucket=self._bucket, Key=key, Body=body, **extra)
        return key
