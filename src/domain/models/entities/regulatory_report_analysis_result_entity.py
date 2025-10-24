from pydantic import BaseModel, Field


class RegulatoryReportAnalysisResultEntity(BaseModel):
    ccr: str = Field(description="Código de crédito")
    difference_from_table: str = Field(description="La diferencia del saldo actual y anterior de la tabla")
    reduced_amount: str = Field(description="Monto reducido / disminuido")
    coincidence: bool = Field(description="Indica si la evaluación de la regla coincide")
