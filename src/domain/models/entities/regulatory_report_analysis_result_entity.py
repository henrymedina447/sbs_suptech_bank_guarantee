from pydantic import BaseModel, Field


class RegulatoryReportAnalysisResultEntity(BaseModel):
    ccr: str = Field(description="Código de crédito")
    difference_from_table: str = Field(description="La cantidad de diferencia de la encontrado en los documentos vs lo "
                                                   "registrado en la tabla")
    reduced_amount: str = Field(description="Monto reducido / disminuido")
    coincidence: bool = Field(description="Indica si la evaluación de la regla coincide")
