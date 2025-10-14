from uuid import UUID

from pydantic import BaseModel, Field

from domain.enums.application_states_enum import ApplicationStatesEnum


class LetterAnalysisData(BaseModel):
    key: str = Field(description="Indica el key obtenido de guardar el archivo en el bucket S3")
    session_id: str = Field(description="Indica la sesión en curso", alias="sessionId")
    period_month: int = Field(description="Período de análisis", alias="periodMonth")
    period_year: int = Field(description="Año de análisis", alias="periodYear")


class AnalysisResultReportEntity(BaseModel):
    """
    Representa el modelo de elemento a guardar de la tabla preferred-warranty-analysis
    """
    source: UUID = Field(description="el uuid que representa la línea de estados")
    id: int = Field(description="id del estado")
    data: LetterAnalysisData = Field(description="Contiene información de metadata")
    event_type: ApplicationStatesEnum | None = Field(description="Contiene el evento",
                                                     default=ApplicationStatesEnum.processed,
                                                     alias="type")
    server_time: str = Field(description="Es el tiempo ISO en el que se envía el evento", alias="time")
    supervised_entity_id: UUID = Field(description="Es el id de la empresa supervisada", alias="supervisedEntityId")

    model_config = {
        "frozen": True
    }
