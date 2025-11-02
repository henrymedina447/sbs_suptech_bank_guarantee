from uuid import UUID

from pydantic import BaseModel, Field


class ParameterContract(BaseModel):
    period_month: int = Field(description="Período de análisis")
    period_year: int = Field(description="Año de análisis")
    legal_name: str = Field(description="Indica la razón social del investigado")
    bank_guarantees: list[str] = Field(description="Ids de Bank guarantees")
    supervised_entity_id: UUID = Field(description="ID de la empresa supervisada")
