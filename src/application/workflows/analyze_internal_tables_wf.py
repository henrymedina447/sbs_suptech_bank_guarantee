import logging
from typing import Any

from langgraph.constants import START, END
from langgraph.graph.state import CompiledStateGraph, StateGraph

from application.exceptions.analyze_data_exception import AnalyzeDataException
from application.states.analyze_data.internal_tables.internal_tables_state import InternalTablesState
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.internal_tables_analysis_result_entity import InternalTablesAnalysisResultEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity
from domain.services.internal_tables_analysis_result_entity_service import InternalTablesAnalysisResultEntityService


class AnalyzeInternalTablesWorkflow:
    def __init__(self):
        self.metadata: list[BankGuaranteeEntity] = []
        self._graph = self._build_graph()
        self.logger = logging.getLogger("app.workflows")

    def _analyze_reduced_amount(self, state: InternalTablesState) -> dict[str, Any]:
        try:
            origin_doc = state.origin_doc
            item: InternalTablesAnalysisResultEntity = InternalTablesAnalysisResultEntityService.get_analyzed_reduced_amount_item(
                origin_doc=origin_doc,
                metadata=self.metadata
            )
            return {
                "internal_tables_analysis_result": item
            }
        except AnalyzeDataException as e:
            self.logger.error(f"""
                                     Se ha producido un error al iniciar el nodo de análisis del
                                     monto reducido en tablas internas de tipo: {e.reason} y mensaje: {e.message}""",
                              exc_info=True)
            return {}
        except Exception as e:
            self.logger.error(f"""
                {e}
            """)
            return {}

    def _build_graph(self) -> CompiledStateGraph[InternalTablesState]:
        g = StateGraph(InternalTablesState)
        g.add_node("analyze_reduced_amount", self._analyze_reduced_amount)
        g.add_edge(START, "analyze_reduced_amount")
        g.add_edge("analyze_reduced_amount", END)
        return g.compile()

    def execute(self,
                origin_doc: InternalTablesEntity,
                metadata: list[BankGuaranteeEntity]
                ) -> InternalTablesState:
        self.metadata = metadata
        state = InternalTablesState(origin_doc=origin_doc)
        out = self._graph.invoke(state)
        return InternalTablesState.model_validate(out)
