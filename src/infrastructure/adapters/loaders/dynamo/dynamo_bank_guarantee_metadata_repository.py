import inspect
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config
from botocore.exceptions import ParamValidationError, EndpointConnectionError, ClientError, ConnectTimeoutError, \
    ReadTimeoutError, BotoCoreError
from mypy_boto3_dynamodb.service_resource import Table, DynamoDBServiceResource
from mypy_boto3_dynamodb.type_defs import QueryOutputTableTypeDef

from application.exceptions.collect_data_exception import CollectDataException
from domain.enums.collect_data_errors_enum import CollectDataErrorsEnum
from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository
from infrastructure.config.app_settings import get_app_settings

INDEX_BY_PERIOD = "period_year-period_month-index"
INDEX_SUPERVISORY_RECORDS = "supervisoryRecordId-index"


class DynamoBankGuaranteeMetadataRepository(BankGuaranteeMetadataRepository):
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

    def get_collection_by_period(self, user_id: str, month: str, year: str) -> list[dict[str, Any]]:
        method_name = inspect.currentframe().f_code.co_name
        try:
            items: list[dict[str, Any]] = []
            response: QueryOutputTableTypeDef = self.table.query(
                IndexName=INDEX_BY_PERIOD,
                KeyConditionExpression=Key("period_year").eq(year) & Key("period_month").eq(month))
            items.extend(response.get("Items", []))
            while "LastEvaluatedKey" in response:
                response = self.table.query(
                    IndexName=INDEX_BY_PERIOD,
                    KeyConditionExpression=Key("period_year").eq(year) & Key("period_month").eq(month),
                    ExclusiveStartKey=response["LastEvaluatedKey"]
                )
                items.extend(response.get("Items", []))
            return items
        except ParamValidationError as e:
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_bank_guarantee_metadata_table,
                message=f"Existen datos mal formados {str(e)} en {method_name}"
            ) from e
        except (EndpointConnectionError, ClientError, ConnectTimeoutError, ReadTimeoutError, BotoCoreError) as e:
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_bank_guarantee_metadata_table,
                message=f"Existe un error crítico al obtener los datos de la tabla en {method_name}"
            ) from e

    def get_collection_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        method_name = inspect.currentframe().f_code.co_name
        try:
            results: list[dict[str, Any]] = []
            # paraleliza 8 hilos (ajusta según tus RCUs)
            with ThreadPoolExecutor(max_workers=4) as ex:
                futures = [ex.submit(self._query_by_supervisory_id, sid) for sid in ids]
                for f in as_completed(futures):
                    results.extend(f.result())

            return results
        except ParamValidationError as e:
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_bank_guarantee_metadata_table,
                message=f"Existen datos mal formados {str(e)} en {method_name}"
            ) from e
        except (EndpointConnectionError, ClientError, ConnectTimeoutError, ReadTimeoutError, BotoCoreError) as e:
            raise CollectDataException(
                reason=CollectDataErrorsEnum.t_bank_guarantee_metadata_table,
                message=f"Existe un error crítico al obtener los datos de la tabla en {method_name}"
            ) from e

    def _query_by_supervisory_id(self, sup_id: str) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        kwargs = dict(
            IndexName=INDEX_SUPERVISORY_RECORDS,
            KeyConditionExpression=Key("supervisoryRecordId").eq(sup_id),
            ProjectionExpression="#id, #md",
            ExpressionAttributeNames={"#id": "id", "#md": "metadata"},
            Limit=100,
        )
        while True:
            resp = self.table.query(**kwargs)
            items.extend(resp.get("Items", []))
            lek = resp.get("LastEvaluatedKey")
            if not lek:
                break
            kwargs["ExclusiveStartKey"] = lek
        return items
