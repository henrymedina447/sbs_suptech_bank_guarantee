import operator
from typing import Annotated

from pydantic import BaseModel, Field

from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity


class CollectDataState(BaseModel):
    internal_tables_collection: Annotated[list[InternalTablesEntity], operator.add] = Field(
        description="Contenido de las tablas internas", default_factory=list)
    regulatory_reports_collection: Annotated[list[RegulatoryReportEntity], operator.add] = Field(
        description="Contenido de los reportes regulatorios", default_factory=list)
    bank_guarantee_metadata_collection: Annotated[list[BankGuaranteeEntity], operator.add] = Field(
        description="Contenido de las meta datas obtenidas", default_factory=list)
