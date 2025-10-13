import logging
from typing import Any

from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph

from application.contracts.parameter_contract import ParameterContract
from application.exceptions.collect_data_exception import CollectDataException
from application.ports.loader_document_port import LoaderDocumentPort
from application.states.collect_data.collect_data_state import CollectDataState
from domain.models.entities.internal_tables_entity import InternalTablesEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity


class CollectDataUseCase:
    def __init__(self, loader_document: LoaderDocumentPort):
        self._loader_document = loader_document
        self._wf_parameters: ParameterContract | None = None
        self._graph = self._build_graph()
        self.logger = logging.getLogger("app.workflows")

    def _load_internal_tables(self, state: CollectDataState) -> dict[str, Any]:
        try:
            results: list[InternalTablesEntity] = self._loader_document.load_internal_tables(self._wf_parameters)
            return {
                "internal_tables_collection": results
            }

        except CollectDataException as e:
            self.logger.error(f"""
                          Se ha producido un error al cargar las tablas internas 
                          de tipo: {e.reason} y mensaje: {e.message}""", exc_info=True)
            return {
                "internal_tables_collection": []
            }

    def _load_regulatory_reports(self, state: CollectDataState) -> dict[str, Any]:
        try:
            results: list[RegulatoryReportEntity] = self._loader_document.load_regulatory_report(self._wf_parameters)
            return {
                "regulatory_reports_collection": results
            }

        except CollectDataException as e:
            self.logger.error(f"""
                          Se ha producido un error al cargar las tablas de reporte regulatorio 
                          de tipo: {e.reason} y mensaje: {e.message}""", exc_info=True)
            return {
                "regulatory_reports_collection": []
            }

    def _load_bank_guarantees_metadata(self, state: CollectDataState) -> dict[str, Any]:
        return {}

    def _build_graph(self) -> CompiledStateGraph[CollectDataState]:
        g = StateGraph(CollectDataState)
        g.add_node("load_internal_tables", self._load_internal_tables)
        g.add_node("load_regulatory_reports", self._load_regulatory_reports)
        g.add_node("load_bank_guarantees_metadata", self._load_bank_guarantees_metadata)
        g.add_edge(START, "load_internal_tables")
        g.add_edge(START, "load_regulatory_reports")
        g.add_edge(START, "load_bank_guarantees_metadata")
        g.add_edge("load_internal_tables", END)
        g.add_edge("load_regulatory_reports", END)
        g.add_edge("load_bank_guarantees_metadata", END)
        return g.compile()

    async def execute(self, parameters: ParameterContract) -> CollectDataState:
        self._wf_parameters = parameters
        state = CollectDataState()
        results = await self._graph.ainvoke(state)
        return CollectDataState.model_validate(results)
