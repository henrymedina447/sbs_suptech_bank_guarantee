from pydantic import BaseModel, Field
from uuid import UUID


class OrchestratorInputContract(BaseModel):
    source: UUID = Field(description="el id del evento")
    type_event: str = Field(description="El tipo de evento que está atendiendo la aplicación")
    analysis_execution_id: str | None = Field(description="Contiene el id de la ejecución", default=None)
    session_id: str = Field(description="Contiene el id de la session")
    id: int = Field(description="Contiene el id del evento")
    supervised_entity_id: UUID = Field(description="Contiene el id de la empresa supervisada")
