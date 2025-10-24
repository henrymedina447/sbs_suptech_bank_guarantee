import logging
from typing import Any
from langgraph.constants import START, END
from langgraph.graph.state import CompiledStateGraph, StateGraph
from application.exceptions.analyze_data_exception import AnalyzeDataException
from application.states.analyze_data.regulatory_reports.regulatory_reports_state import RegulatoryReportState
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.fmv_guarantee_letters_result_entity import FMVGuaranteeLettersResultEntity
from domain.models.entities.regulatory_report_analysis_result_entity import RegulatoryReportAnalysisResultEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity
from domain.services.regulatory_report_analysis_result_entity_service import RegulatoryReportAnalysisResultEntityService


class AnalyzeRegulatoryReportWorkflow:

    def __init__(self):
        self.metadata: list[BankGuaranteeEntity] = []
        self._graph = self._build_graph()
        self.logger = logging.getLogger("app.workflows")

    def _analyze_reduced_amount(self, state: RegulatoryReportState) -> dict[str, Any]:
        """
               Evalúa la regla:La suma de todos los montos reducidos de las cartas que están asociadas a un código de
               crédito en un mismo período debe ser igual al monto reducido calculado que existe en la misma fila
               del código de garantía que se revisa.
               :param state:
               :return:
        """
        try:
            origin_doc = state.origin_doc
            item: RegulatoryReportAnalysisResultEntity = RegulatoryReportAnalysisResultEntityService.get_analyzed_reduced_amount_item(
                origin_doc=origin_doc,
                metadata=self.metadata,
            )
            return {
                "regulatory_report_analysis_result": item
            }
        except AnalyzeDataException as e:
            self.logger.error(f"""
                              Se ha producido un error al iniciar el nodo de análisis del
                              monto reducido en reportes regulatorios de tipo: {e.reason} y mensaje: {e.message}""",
                              exc_info=True)
            return {}

    def _analyze_fmv_guarantee_letters(self, state: RegulatoryReportState) -> dict[str, Any]:
        """
        Evalúa la regla compuesta: - (1) Dado un código de crédito; obtener el nombre del cliente en la tabla de
        reportes regulatorios; - (2) Dado un código de crédito; obtener todas las cartas que compartan el mismo
        número de crédito en los metadatos - Hecho el punto 1 y 2 se revisa la regla: Todas las cartas asociadas a un
        código de crédito deben tener el mismo nombre de cliente dentro de la metadata
        :param state:
        :return:
        """
        try:
            origin_doc = state.origin_doc
            item: list[
                FMVGuaranteeLettersResultEntity] = RegulatoryReportAnalysisResultEntityService.get_analyze_fmv_guarantee_letters_item(
                origin_doc=origin_doc,
                metadata=self.metadata,
            )
            return {
                "fmv_guarantee_letter_result": item
            }
        except AnalyzeDataException as e:
            self.logger.error(f"""
                                          Se ha producido un error al iniciar el nodo de análisis de
                                          la igualdad de cartas de tipo: {e.reason} y mensaje: {e.message}""",
                              exc_info=True)
            return {}

    def _build_graph(self) -> CompiledStateGraph[RegulatoryReportState]:
        g = StateGraph(RegulatoryReportState)
        g.add_node("analyze_reduced_amount", self._analyze_reduced_amount)
        g.add_node("analyze_fmv_guarantee_letters", self._analyze_fmv_guarantee_letters)
        g.add_edge(START, "analyze_reduced_amount")
        g.add_edge("analyze_reduced_amount", "analyze_fmv_guarantee_letters")
        g.add_edge("analyze_fmv_guarantee_letters", END)
        return g.compile()

    def execute(self,
                origin_doc: RegulatoryReportEntity,
                metadata: list[BankGuaranteeEntity]
                ) -> RegulatoryReportState:
        self.metadata = metadata
        state = RegulatoryReportState(origin_doc=origin_doc)
        out = self._graph.invoke(state)
        return RegulatoryReportState.model_validate(out)
