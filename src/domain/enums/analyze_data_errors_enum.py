from enum import StrEnum


class AnalyzeDataErrorEnum(StrEnum):
    start_task_service = "Error al ejecutar una operación en start task "
    analyzed_reduced_amount = "Error al verificar la regla de monto reducido"
    analyzed_fmv_guarantee = "Error, no existen datos dentro del calculo de la similitud de clientes en cartas"
