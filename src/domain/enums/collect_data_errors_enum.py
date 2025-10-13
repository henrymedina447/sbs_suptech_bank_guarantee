from enum import StrEnum


class CollectDataErrorsEnum(StrEnum):
    t_internal_table = "Error al ejecutar una operación en la tabla interna del investigado"
    t_regulatory_report = "Error al ejecutar una operación en la tabla de reporte regulatorio"
    u_internal_table = "Error al ejecutar una transformación en la tabla interna del investigado"
    u_regulatory_report = "Error al ejecutar una transformación en la tabla de reporte regulatorios"

