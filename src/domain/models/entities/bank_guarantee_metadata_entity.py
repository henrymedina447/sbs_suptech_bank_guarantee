from pydantic import BaseModel, Field


class MetadataEntity(BaseModel):
    letter_date: str | None = Field(description="Contiene la fecha en que se realizó la carta", default=None)
    disbursed_amount: float | None = Field(description="Contiene el monto desembolsado", default=None)
    reduced_amount: float | None = Field(description="Contiene el monto disminuido", default=None)
    total_amount: float | None = Field(description="Contiene el monto total", default=None)
    letter_text: str | None = Field(description="Contiene el número de la carta", default=None)
    project_text: str | None = Field(description="Contiene el nombre del proyecto", default=None)


class BankGuaranteeEntity(BaseModel):
    file_name: str = Field(description="Nombre del archivo")
    period_month: str = Field(description="mes del periodo")
    period_year: str = Field(description="Año del periodo")
    supervisory_record_id: str = Field(description="ID del documento en los records generales")
    type_document: str = Field(description="Tipo del documento", default="carta fianza")
    metadata: MetadataEntity | None = Field(description="Metadatos del documento")
