from datetime import datetime

from application.contracts.parameter_contract import ParameterContract
from application.states.orchestrator_state import OrchestratorState
from domain.enums.application_states_enum import ApplicationStatesEnum
from domain.models.entities.analysis_result_report_entity import AnalysisResultReportEntity, LetterAnalysisData


class OrchestratorWorkflowDomainService:

    @staticmethod
    def get_analysis_report_entity(
            key: str,
            state: OrchestratorState,
            parameters: ParameterContract
    ) -> AnalysisResultReportEntity:
        """
                Obtiene el payload a guardar en la salida de la base de datos dynamo
                :param key: Ubicación del archivo en el bucket
                :param parameters:
                :param state: Estado del orquestador general
                :return:
                """
        server_time = datetime.now().isoformat(timespec="seconds").replace("+00:00", "Z")
        return AnalysisResultReportEntity(
            source=state.source,
            id=int(state.id) + 1,
            data=LetterAnalysisData(
                key=key,
                sessionId=state.session_id,
                periodMonth=parameters.period_month,
                periodYear=parameters.period_year,
            ),
            type=ApplicationStatesEnum.processed,
            time=server_time,
            supervisedEntityId=state.supervised_entity_id
        )
