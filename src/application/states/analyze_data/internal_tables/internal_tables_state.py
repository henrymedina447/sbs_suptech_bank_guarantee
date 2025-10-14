from pydantic import BaseModel, Field

from domain.models.entities.internal_tables_analysis_result_entity import InternalTablesAnalysisResultEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity


class InternalTablesState(BaseModel):
    origin_doc: InternalTablesEntity = Field(description="Fila original proveniente de la tabla interna")
    internal_tables_analysis_result: InternalTablesAnalysisResultEntity | None = Field(
        description="Fila de la tabla de reporte ", default=None
    )
