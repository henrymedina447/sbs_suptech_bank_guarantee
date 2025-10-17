from pydantic import BaseModel, Field


class MetadataByIdEntity(BaseModel):
    file_name: str = Field(description="Nombre del archivo")
    letter_date: str | None = Field(description="Contiene la fecha en que se realizó la carta", default=None)
    disbursed_amount: float | None = Field(description="Contiene el monto desembolsado", default=None)
    reduced_amount: float | None = Field(description="Contiene el monto disminuido", default=None)
    total_amount: float | None = Field(description="Contiene el monto total", default=None)
    letter_text: str | None = Field(description="Contiene el número de la carta", default=None)
    project_text: str | None = Field(description="Contiene el nombre del proyecto", default=None)
    promotor: str | None = Field(description="Contiene el nombre del promotor / cliente", default=None)
    period_month: str = Field(description="mes del periodo")
    period_year: str = Field(description="Año del periodo")


class BankGuaranteeMetadataByIdEntity(BaseModel):
    id: str = Field(description="Id del documento")
    supervisory_record_id: str = Field(description="Id del documento desde el record", alias="supervisoryRecordId")
    metadata: MetadataByIdEntity | None = Field(description="Metadatos del documento", default=None)
