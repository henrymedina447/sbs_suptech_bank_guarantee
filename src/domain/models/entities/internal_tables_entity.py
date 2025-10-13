from pydantic import Field, BaseModel


class InternalTablesEntity(BaseModel):
    id: str = Field(description="ID de la regulatory report entity")
    period_year: int = Field(description="Indica el periodo en año")
    period_month: int = Field(description="Indica el periodo en mes")
    currency: str = Field(description="Indica la monde de los montos")
    codigo_credito: str = Field(description="Código de crédito sobre el cual se itera")
    codigo_cliente: str = Field(description="Código del cliente")
    saldo: float = Field(description="Monto del mes actual")
    saldo_mes_anterior: float | None = Field(description="Monto del mes anterior", default=None)
