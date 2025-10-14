import operator
from typing import Annotated

from pydantic import BaseModel, Field
from domain.models.entities.fmv_guarantee_letters_result_entity import FMVGuaranteeLettersResultEntity
from domain.models.entities.regulatory_report_analysis_result_entity import RegulatoryReportAnalysisResultEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity


class RegulatoryReportState(BaseModel):
    origin_doc: RegulatoryReportEntity = Field(description="Fila original proveniente de la tabla de reporte "
                                                           "regulatorio")
    fmv_guarantee_letter_result: list[FMVGuaranteeLettersResultEntity] = Field(
        description="Contiene el resultado del análisis de la coincidencia del nombre del cliente en todas las cartas "
                    "asociadas a él",
        default_factory=list,
    )
    regulatory_report_analysis_result: RegulatoryReportAnalysisResultEntity | None = Field(
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
