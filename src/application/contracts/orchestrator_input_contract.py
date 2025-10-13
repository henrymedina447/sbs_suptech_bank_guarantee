from pydantic import BaseModel, Field
from uuid import UUID


class OrchestratorInputContract(BaseModel):
    source: UUID = Field(description="el id del evento")
    type_event: str = Field(description="El tipo de evento que está atendiendo la aplicación")
    analysis_execution_id: str = Field(description="Contiene el id de la ejecución")
    session_id: str = Field(description="Contiene el id de la session")
