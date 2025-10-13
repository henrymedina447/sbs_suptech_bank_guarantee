from pydantic import Field
from application.contracts.orchestrator_input_contract import OrchestratorInputContract
from application.states.analyze_data.analyse_data_state import AnalyzeDataState
from application.states.collect_data.collect_data_state import CollectDataState


class OrchestratorState(OrchestratorInputContract):
    collect_data: CollectDataState | None = Field(
        description="Todos los datos obtenidos desde las fuentes de dynamo",
        default=None
    )
    analyze_data: AnalyzeDataState | None = Field(
        description="Todos los datos obtenidos producto del motor de reglas",
        default=None
    )
