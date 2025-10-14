from pydantic import BaseModel, Field


class FMVGuaranteeLettersResultEntity(BaseModel):
    ccr: str = Field(description="Código de crédito")
    letter_text: str | None = Field(description="Contiene el número de la carta", default=None)
    client_origin: str = Field(description="Nombre del cliente desde la tabla de reporte")
    client_metadata: str | None = Field(description="Nombre del cliente desde la metadata", default=None)
    coincidence: bool = Field(description="Indica si la evaluación de la regla coincide")
