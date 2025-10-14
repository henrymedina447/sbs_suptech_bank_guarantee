import logging
from typing import Any

from langgraph.constants import START, END
from langgraph.graph.state import CompiledStateGraph, StateGraph

from application.contracts.orchestrator_input_contract import OrchestratorInputContract
from application.contracts.parameter_contract import ParameterContract
from application.ports.loader_document_port import LoaderDocumentPort
from application.ports.messaging_status_port import MessagingStatusPort
from application.states.analyze_data.analyse_data_state import AnalyzeDataState
from application.states.collect_data.collect_data_state import CollectDataState
from application.states.orchestrator_state import OrchestratorState
from application.uses_cases.analyze_data_uc import AnalyzeDataUseCase
from application.uses_cases.collect_data_uc import CollectDataUseCase
from application.services.orchestrator_wf_domain_service import OrchestratorWorkflowDomainService
from domain.models.entities.analysis_result_report_entity import AnalysisResultReportEntity


class OrchestratorWorkflow:
    def __init__(self,
                 collect_data_uc: CollectDataUseCase,
                 analyze_data_uc: AnalyzeDataUseCase,
                 loader_document: LoaderDocumentPort,
                 messaging: MessagingStatusPort
                 ):
        self._collect_data_uc = collect_data_uc
        self._analyze_data_uc = analyze_data_uc
        self._loader_document = loader_document
        self._messaging = messaging
        self._logger = logging.getLogger("app.workflows")
        self._graph = self._build_graph()
        self.wf_parameters: ParameterContract | None = None

    def _start_task(self, state: OrchestratorState) -> dict[str, Any]:
        """
        Inicia tareas de preparación si se requiere
        :param state:
        :return:
        """
        self._logger.info("start task running")
        return {}

    async def _collect_data(self, state: OrchestratorState) -> dict[str, Any]:
        """
        Inicia todas las tareas de recolección de data de todas las fuentes registradas
        :param state:
        :return:
        """
        self._logger.info("collect data running")
        results: CollectDataState = await self._collect_data_uc.execute(self.wf_parameters)
        return {
            "collect_data": results,
        }

    async def _analyze_data(self, state: OrchestratorState) -> dict[str, Any]:
        """
        Inicia todas las tareas de análisis de reglas
        :param state:
        :return:
        """
        self._logger.info("analyze data running")
        collections: CollectDataState = state.collect_data
        results: AnalyzeDataState = await self._analyze_data_uc.execute(self.wf_parameters, collections)
        return {
            "analyze_data": results,
        }

    def _final_task(self, state: OrchestratorState) -> dict[str, Any]:
        """
        Realiza tareas de registro y comunicación de eventos de los resultados obtenidos del análisis
        :param state:
        :return:
        """
        self._logger.info("final task running")
        # Guardar en S3
        bucket_success, key = self._loader_document.save_analysis(state.source, state.analyze_data)
        if not bucket_success:
            self._logger.error(f"error al iniciar el proceso de guardado en el bucket")
            return {}
        payload_to_report: AnalysisResultReportEntity = OrchestratorWorkflowDomainService.get_analysis_report_entity(
            key,
            state,
            self.wf_parameters
        )
        # Guardar en dynamo
        self._loader_document.save_status(payload_to_report)

        # Comunicar a sqs
        self._messaging.publish_status(payload_to_report)
        return {}

    def _build_graph(self) -> CompiledStateGraph[OrchestratorState]:
        g = StateGraph(OrchestratorState)
        # Declaración de nodos
        g.add_node("start_task", self._start_task)
        g.add_node("collect_data", self._collect_data)
        g.add_node("analyze_data", self._analyze_data)
        g.add_node("final_task", self._final_task)
        # Declaración de aristas
        g.add_edge(START, "start_task")
        g.add_edge("start_task", "collect_data")
        g.add_edge("collect_data", "analyze_data")
        g.add_edge("analyze_data", "final_task")
        g.add_edge("final_task", END)
        return g.compile()

    async def execute(self, wf_input: OrchestratorInputContract, wf_parameters: ParameterContract) -> None:
        self._logger.info("execute running")
        self.wf_parameters = wf_parameters
        state: OrchestratorState = OrchestratorState(**wf_input.model_dump())
        await self._graph.ainvoke(state)
