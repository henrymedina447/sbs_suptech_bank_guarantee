from pydantic import BaseModel, Field


class RegulatoryReportEntity(BaseModel):
    id: str = Field(description="ID de la regulatory report entity")
    period_year: int = Field(description="Indica el periodo en año")
    period_month: int = Field(description="Indica el periodo en mes")
    currency: str = Field(description="Indica la monde de los montos")
    ccr: str = Field(description="Código de crédito sobre el cual se itera")
    ccl: str = Field(description="Código del cliente")
    csbs: str = Field(description="Código del cliente que asigna la sbs")
    ncl: str | None = Field(description="Desconocido", default=None)
    kco: float = Field(description="Monto del mes actual")
    ccco: str = Field(description="Desconocido")
    ccco_mes_anterior: str | None = Field(description="Desconocido", default=None)
    kco_mes_anterior: float | None = Field(description="Monto del mes anterior", default=0)
    convenio_fmv: str | None = Field(
        description="Indica si el ccr tiene un convenio con el fondo mi vivienda (Sí)",
        default=None
    )
