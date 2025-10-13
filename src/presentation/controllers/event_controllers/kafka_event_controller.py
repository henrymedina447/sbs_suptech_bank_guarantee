import asyncio
import json
import logging
from typing import Any
from aiokafka import AIOKafkaConsumer
from pydantic import ValidationError

from application.contracts.orchestrator_input_contract import OrchestratorInputContract
from application.contracts.parameter_contract import ParameterContract
from infrastructure.bootstrap.container import build_workflow
from infrastructure.config.app_settings import KafkaSettings, get_app_settings
from presentation.dto.requests.analyze_request_dto import AnalyzeRequestDto

app_logger = logging.getLogger("app.environment")


class KafkaEventController:
    def __init__(self, max_concurrency: int = 8):
        self._wf = build_workflow()
        self._consumer: AIOKafkaConsumer | None = None
        self._stopping = asyncio.Event()
        self._sem = asyncio.Semaphore(max_concurrency)

    @staticmethod
    def _get_kafka_config() -> dict[str, Any]:
        k: KafkaSettings = get_app_settings().kafka_settings
        cfg: dict[str, Any] = {
            "bootstrap_servers": k.bootstrap_servers,
            "group_id": k.group_id,
            "security_protocol": k.security_protocol,
        }
        return cfg

    @staticmethod
    def _get_kafka_topic() -> str:
        k: KafkaSettings = get_app_settings().kafka_settings
        return k.topic

    @staticmethod
    async def create_consumer() -> AIOKafkaConsumer:
        cfg = KafkaEventController._get_kafka_config()
        topic = KafkaEventController._get_kafka_topic()
        consumer = AIOKafkaConsumer(topic, **cfg)
        await consumer.start()
        return consumer

    async def start(self) -> None:
        self._consumer = await KafkaEventController.create_consumer()
        asyncio.create_task(self._loop())

    async def stop(self) -> None:
        self._stopping.set()
        if self._consumer:
            await self._consumer.stop()

    async def _loop(self) -> None:
        c = self._consumer
        try:
            while not self._stopping.is_set():
                batches = await c.getmany(timeout_ms=1000, max_records=10)
                tasks = []
                for _tp, msgs in batches.items():
                    for m in msgs:
                        tasks.append(asyncio.create_task(self._handle(m.value)))
                if tasks:
                    await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            await c.stop()

    async def _handle(self, value: bytes) -> None:
        async with self._sem:
            try:
                text = value.decode("utf-8", errors="ignore")
                data = json.loads(text) if text else {}
                dto: AnalyzeRequestDto = AnalyzeRequestDto.model_validate(data)
                wf_input: OrchestratorInputContract = OrchestratorInputContract(
                    analysis_execution_id=dto.analysis_execution_id,
                    type_event=dto.type_event,
                    source=dto.source,
                    session_id=dto.data.session_id,
                )
                wf_parameters: ParameterContract = ParameterContract(
                    period_year=dto.data.period_year,
                    period_month=dto.data.period_month,
                    legal_name=dto.data.supervised_entity.legal_name,
                    bank_guarantees=dto.data.bank_guarantees
                )
                return await asyncio.to_thread(self._wf.execute, wf_input, wf_parameters)

            except ValidationError as e:
                app_logger.exception(f"Error de validación: {str(e)}")
            except Exception as e:
                app_logger.exception(f"Error procesando mensaje kafka {str(e)}")
