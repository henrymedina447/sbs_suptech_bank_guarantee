from pydantic import BaseModel, Field
from uuid import UUID


class SupervisedEntityDto(BaseModel):
    legal_name: str = Field(description="Indica la razón social del investigado", alias="legalName")


class DataInputDto(BaseModel):
    supervised_entity: SupervisedEntityDto = Field(description="Contiene toda la información de la entidad supervisada",
                                                   alias="supervisedEntity")
    bank_guarantees: list[str] = Field(description="Contienen todos los id de los documentos de carta fianzas ")
    analysis_execution_id: str = Field(description="Indica el id de análisis", alias="analysisExecutionId")
    period_month: int = Field(description="Período de análisis", alias="periodMonth", ge=1, le=12)
    period_year: int = Field(description="Año de análisis", alias="periodYear", ge=1990, le=2050)
    session_id: str = Field(description="Indica la sesión en curso", alias="sessionId")


class AnalyzeRequestDto(BaseModel):
    """
    Representa el request de la API
    """
    source: UUID = Field(description="el uuid que representa la línea de estados")
    id: int = Field(description="id del estado")
    type_event: str = Field(description="El tipo de evento que está atendiendo la aplicación", alias="type")
    data: DataInputDto = Field(description="Contiene data parametrizada y dinámica del lado del usuario")
    server_time: str = Field(description="Indica el tiempo del servidor", alias="time")
    supervised_entity_id: UUID = Field(description="Es el id de la empresa supervisada", alias="supervisedEntityId")
