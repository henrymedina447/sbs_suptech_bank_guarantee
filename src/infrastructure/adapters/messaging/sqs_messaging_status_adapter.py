import json
from typing import Any
from urllib.parse import urlparse

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from pydantic import BaseModel

from application.ports.messaging_status_port import MessagingStatusPort
from domain.models.entities.analysis_result_report_entity import AnalysisResultReportEntity
from infrastructure.config.app_settings import AppSettings, get_app_settings


class SqsMessagingStatusAdapter(MessagingStatusPort):
    def __init__(self):
        self._app_settings: AppSettings = get_app_settings()
        self.queue_url = self._app_settings.sqs_settings.queue_url
        self.client = self.sqs_client()

    def _region_from_queue_url(self, queue_url: str) -> str:
        """
        Extrae la región de la URL de la cola.
        ej: https://sqs.us-east-1.amazonaws.com/123456789012/mi-cola
        """
        host = urlparse(queue_url).netloc  # sqs.us-east-1.amazonaws.com
        return host.split(".")[1]

    def sqs_client(self):
        """
        Devuelve un cliente boto3 de SQS.
        Si la región no está en settings, se infiere de la URL.
        """
        _cfg = Config(
            retries={"max_attempts": 10, "mode": "standard"},
            connect_timeout=3,
            read_timeout=5
        )

        sqs_settings = get_app_settings().sqs_settings
        region = self._region_from_queue_url(sqs_settings.queue_url) or self._app_settings.aws_settings.region
        return boto3.client("sqs", region_name=region, config=_cfg)

    def publish_status(self, status: AnalysisResultReportEntity) -> None:
        body_to_send: str=""
        if isinstance(status, BaseModel):
            body_to_send = status.model_dump_json(by_alias=True)
        elif not isinstance(status, str):
            body_to_send = json.dumps(status, ensure_ascii=False)
        params: dict[str, Any] = {
            "QueueUrl": self.queue_url,
            "MessageBody": body_to_send
        }

        try:
            resp = self.client.send_message(**params)
            return resp["MessageId"]
        except ClientError as e:
            # Agregar un error
            raise
        except Exception as e:
            print(f"error: {e}")
