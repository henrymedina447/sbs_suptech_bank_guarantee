from pydantic import BaseModel, Field
from application.states.analyze_data.regulatory_reports.fmv_guarantee_letters_result_state import FMVGuaranteeLettersResultState
from application.states.analyze_data.internal_tables.internal_tables_analysis_result_state import InternalTablesAnalysisResultState


class AnalyzeDataState(BaseModel):
    fmv_guarantee_letter_result: FMVGuaranteeLettersResultState | None = Field(
        description="Contiene el resultado del análisis de la coincidencia del nombre del cliente en todas las cartas "
                    "asociadas a él",
        default=None

    )
    internal_tables_analysis_result: InternalTablesAnalysisResultState | None = Field(
        description="Contiene el resultado del análisis de la"
                    "coincidencia del cálculo del monto de las "
                    "reducciones encontrado en los documentos vs lo "
                    "registrado en la tabla interna en el mes y año "
                    "investigado",
        default=None

    )
    regulatory_report_analysis_result: InternalTablesAnalysisResultState | None = Field(
        description="Contiene el resultado del "
                    "análisis de la "
                    "coincidencia del cálculo "
                    "del monto de las "
                    "reducciones encontrado en "
                    "los documentos vs lo "
                    "registrado en la tabla "
                    "interna en el mes y año "
                    "investigado",
        default=None)

