from pydantic import BaseModel, Field


class FMVGuaranteeLettersResultState(BaseModel):
    ccr: str = Field(description="Código de crédito")
    letter_text: str = Field(description="Contiene el número de la carta", default=None)
    reduced_amount: str = Field(description="Monto reducido / disminuido")
    coincidence: bool = Field(description="Indica si la evaluación de la regla coincide")
