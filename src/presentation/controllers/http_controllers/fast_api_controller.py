from fastapi import FastAPI, Depends
from application.contracts.orchestrator_input_contract import OrchestratorInputContract
from application.contracts.parameter_contract import ParameterContract
from application.uses_cases.orchestrator_uc import OrchestratorWorkflow
from infrastructure.bootstrap.container import build_workflow
from presentation.dto.requests.analyze_request_dto import AnalyzeRequestDto

app = FastAPI(title="SBS ETL API")


def get_factory() -> OrchestratorWorkflow:
    return build_workflow()


@app.post("/start-analysis")
async def run_analysis(dto: AnalyzeRequestDto, wf: OrchestratorWorkflow = Depends(get_factory)):
    try:
        wf_input: OrchestratorInputContract = OrchestratorInputContract(
            analysis_execution_id=dto.data.analysis_execution_id,
            type_event=dto.type_event,
            source=dto.source,
            session_id=dto.data.session_id,
            id=dto.id,
            supervised_entity_id=dto.data.supervised_entity.supervised_entity_id,
        )
        wf_parameters: ParameterContract = ParameterContract(
            period_year=dto.data.period_year,
            period_month=dto.data.period_month,
            legal_name=dto.data.supervised_entity.legal_name,
            bank_guarantees=dto.data.bank_guarantees,
            supervised_entity_id=dto.data.supervised_entity.supervised_entity_id,
        )
        await wf.execute(wf_input, wf_parameters)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
