import logging
from typing import Any

from langgraph.constants import START, END
from langgraph.graph.state import CompiledStateGraph, StateGraph

from application.contracts.parameter_contract import ParameterContract
from application.exceptions.analyze_data_exception import AnalyzeDataException
from application.services.analyze_data_application_service import AnalyzeDataApplicationService
from application.states.analyze_data.analyse_data_state import AnalyzeDataState
from application.states.analyze_data.internal_tables.internal_tables_state import InternalTablesState
from application.states.analyze_data.regulatory_reports.regulatory_reports_state import RegulatoryReportState
from application.states.collect_data.collect_data_state import CollectDataState
from application.workflows.analyze_internal_tables_wf import AnalyzeInternalTablesWorkflow
from application.workflows.analyze_regulatory_reports_wf import AnalyzeRegulatoryReportWorkflow
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.fmv_guarantee_letters_result_entity import FMVGuaranteeLettersResultEntity
from domain.models.entities.internal_tables_analysis_result_entity import InternalTablesAnalysisResultEntity
from domain.models.entities.regulatory_report_analysis_result_entity import RegulatoryReportAnalysisResultEntity


class AnalyzeDataUseCase:
    def __init__(self):
        self._graph = self._build_graph()
        self.logger = logging.getLogger("app.workflows")
        self._wf_parameters: ParameterContract | None = None
        self.collections: CollectDataState | None = None
        self.bank_guarantee_metadata_normalized: list[BankGuaranteeEntity] = []
        self.rr_wf: AnalyzeRegulatoryReportWorkflow = AnalyzeRegulatoryReportWorkflow()
        self.it_wf: AnalyzeInternalTablesWorkflow = AnalyzeInternalTablesWorkflow()

    def _start_task(self, state: AnalyzeDataState) -> dict[str, Any]:
        """
        Nodo encargado de la preparación de la data antes de ser procesada por el flujo
        :param state:
        :return:
        """
        try:
            self.bank_guarantee_metadata_normalized = AnalyzeDataApplicationService.normalize_bank_guarantee_metadata(
                self.collections.bank_guarantee_metadata_collection
            )
            return {}
        except AnalyzeDataException as e:
            self.logger.error(f"""
                                   Se ha producido un error al iniciar al iniciar el nodo start_task 
                                   de tipo: {e.reason} y mensaje: {e.message}""", exc_info=True)
            return {}

    def _analyze_regulatory_reports(self, state: AnalyzeDataState) -> dict[str, Any]:
        """
        Resuelve todos los procesos de las reglas de los reportes regulatorios
        :param state:
        :return:
        """
        try:
            results_1: list[FMVGuaranteeLettersResultEntity] = []
            results_2: list[RegulatoryReportAnalysisResultEntity] = []
            for rr in self.collections.regulatory_reports_collection:
                if rr.convenio_fmv is None:
                    continue
                result: RegulatoryReportState = self.rr_wf.execute(
                    origin_doc=rr,
                    metadata=self.bank_guarantee_metadata_normalized)
                results_1.extend(result.fmv_guarantee_letter_result)
                results_2.append(result.regulatory_report_analysis_result)

            return {
                "fmv_guarantee_letter_results": results_1,
                "regulatory_report_analysis_results": results_2,
            }
        except AnalyzeDataException as e:
            self.logger.error(f"""
                                              Se ha producido un error en el análisis del reporte regulatorio 
                                              de tipo: {e.reason} y mensaje: {e.message}""", exc_info=True)
            return {}

    def _analyze_internal_tables(self, state: AnalyzeDataState) -> dict[str, Any]:
        """
        Resuelve todos los procesos de las internal tables
        :param state:
        :return:
        """
        try:
            results_1: list[InternalTablesAnalysisResultEntity] = []
            for it in self.collections.internal_tables_collection:
                result: InternalTablesState = self.it_wf.execute(
                    origin_doc=it,
                    metadata=self.bank_guarantee_metadata_normalized
                )
                results_1.append(result.internal_tables_analysis_result)
            return {
                "internal_tables_analysis_results": results_1,
            }
        except AnalyzeDataException as e:
            self.logger.error(f"""
                                                     Se ha producido un error en el análisis de las tablas de interna 
                                                     de tipo: {e.reason} y mensaje: {e.message}""", exc_info=True)
            return {}

    def _build_graph(self) -> CompiledStateGraph[AnalyzeDataState]:
        g = StateGraph(AnalyzeDataState)
        g.add_node("start_task", self._start_task)
        g.add_node("analyze_regulatory_reports", self._analyze_regulatory_reports)
        g.add_node("analyze_internal_tables", self._analyze_internal_tables)
        g.add_edge(START, "start_task")
        g.add_edge("start_task", "analyze_regulatory_reports")
        g.add_edge("analyze_regulatory_reports", "analyze_internal_tables")
        g.add_edge("analyze_internal_tables", END)
        return g.compile()

    async def execute(self, parameters: ParameterContract, collections: CollectDataState) -> AnalyzeDataState:
        self._wf_parameters = parameters
        self.collections = collections
        state = AnalyzeDataState()
        results = await self._graph.ainvoke(state)
        return AnalyzeDataState.model_validate(results)
