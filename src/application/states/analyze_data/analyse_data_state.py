from pydantic import BaseModel, Field
from domain.models.entities.fmv_guarantee_letters_result_entity import FMVGuaranteeLettersResultEntity
from domain.models.entities.internal_tables_analysis_result_entity import InternalTablesAnalysisResultEntity
from domain.models.entities.regulatory_report_analysis_result_entity import RegulatoryReportAnalysisResultEntity


class AnalyzeDataState(BaseModel):
    fmv_guarantee_letter_results: list[FMVGuaranteeLettersResultEntity] = Field(
        description="Contiene el resultado del análisis de la coincidencia del nombre del cliente en todas las cartas "
                    "asociadas a él",
        default_factory=list

    )
    internal_tables_analysis_results: list[InternalTablesAnalysisResultEntity] = Field(
        description="Contiene el resultado del análisis de la"
                    "coincidencia del cálculo del monto de las "
                    "reducciones encontrado en los documentos vs lo "
                    "registrado en la tabla interna en el mes y año "
                    "investigado",
        default_factory=list

    )
    regulatory_report_analysis_results: list[RegulatoryReportAnalysisResultEntity] = Field(
        description="Contiene el resultado del "
                    "análisis de la "
                    "coincidencia del cálculo "
                    "del monto de las "
                    "reducciones encontrado en "
                    "los documentos vs lo "
                    "registrado en la tabla "
                    "interna en el mes y año "
                    "investigado",
        default_factory=list)

