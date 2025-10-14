import inspect

import boto3
from botocore.config import Config
from botocore.exceptions import ParamValidationError, EndpointConnectionError, ClientError, ConnectTimeoutError, \
    ReadTimeoutError, BotoCoreError
from mypy_boto3_dynamodb.service_resource import Table, DynamoDBServiceResource

from application.exceptions.collect_data_exception import CollectDataException
from domain.enums.collect_data_errors_enum import CollectDataErrorsEnum
from domain.models.entities.analysis_result_report_entity import AnalysisResultReportEntity
from domain.repositories.analysis_result_report_status_repository import AnalysisResultReportStatusRepository
from infrastructure.config.app_settings import get_app_settings


class DynamoAnalysisResultStatusRepository(AnalysisResultReportStatusRepository):
    def __init__(self):
        self.app_settings = get_app_settings()
        dynamo_resource = self._get_configuration()

        self.table: Table = dynamo_resource.Table(
            self.app_settings.table_settings.si_table
        )

    def _get_configuration(self) -> DynamoDBServiceResource:
        _cfg = Config(
            retries={"max_attempts": 10, "mode": "standard"},
            connect_timeout=3,
            read_timeout=5,
        )
        return boto3.resource(
            "dynamodb", config=_cfg, region_name=self.app_settings.aws_settings.region
        )

    def save_status(self, result: AnalysisResultReportEntity) -> None:
        item = result.model_dump(mode="json", by_alias=True)
        item["source"] = str(item["source"])  # por si acaso
        item["id"] = str(item["id"])
        method_name = inspect.currentframe().f_code.co_name
        try:
            self.table.put_item(Item=item)
        except ParamValidationError as e:
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_analysis_result,
                message=f"Existen datos mal formados {str(e)} en {method_name}"
            ) from e
        except (EndpointConnectionError, ClientError, ConnectTimeoutError, ReadTimeoutError, BotoCoreError) as e:
            print(f"error: {e}")
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_analysis_result,
                message=f"Existe un error crítico al obtener los datos de la tabla en {method_name}"
            ) from e
