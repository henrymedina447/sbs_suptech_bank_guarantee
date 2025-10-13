import inspect
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config
from botocore.exceptions import ParamValidationError, EndpointConnectionError, ClientError, ConnectTimeoutError, \
    ReadTimeoutError, BotoCoreError
from mypy_boto3_dynamodb.service_resource import DynamoDBServiceResource, Table
from mypy_boto3_dynamodb.type_defs import QueryOutputTableTypeDef

from application.exceptions.collect_data_exception import CollectDataException
from domain.enums.collect_data_errors_enum import CollectDataErrorsEnum
from domain.repositories.internal_tables_repository import InternalTablesRepository
from infrastructure.config.app_settings import get_app_settings

INDEX = "period_year-period_month-index"


class DynamoInternalTablesRepository(InternalTablesRepository):
    def __init__(self):
        self.app_settings = get_app_settings()
        dynamo_resource = self._get_configuration()

        self.table: Table = dynamo_resource.Table(
            self.app_settings.table_settings.it_table
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

    def get_collection(self, user_id: str, month: str, year: str) -> list[dict[str, Any]]:
        method_name = inspect.currentframe().f_code.co_name
        try:
            items: list[dict[str, Any]] = []
            response: QueryOutputTableTypeDef = self.table.query(
                IndexName=INDEX,
                KeyConditionExpression=Key("period_year").eq(int(year)) & Key("period_month").eq(int(month)))
            items.extend(response.get("Items", []))
            while "LastEvaluatedKey" in response:
                response = self.table.query(
                    IndexName=INDEX,
                    KeyConditionExpression=Key("period_year").eq(year) & Key("period_month").eq(month),
                    ExclusiveStartKey=response["LastEvaluatedKey"]
                )
                items.extend(response.get("Items", []))
            return items
        except ParamValidationError as e:
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_internal_table,
                message=f"Existen datos mal formados {str(e)} en {method_name}"
            ) from e
        except (EndpointConnectionError, ClientError, ConnectTimeoutError, ReadTimeoutError, BotoCoreError) as e:
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_internal_table,
                message=f"Existe un error crítico al obtener los datos de la tabla en {method_name}"
            ) from e
