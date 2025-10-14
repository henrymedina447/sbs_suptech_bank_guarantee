import inspect

from pydantic import ValidationError

from application.exceptions.analyze_data_exception import AnalyzeDataException
from domain.enums.analyze_data_errors_enum import AnalyzeDataErrorEnum
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity


class AnalyzeDataApplicationService:

    @staticmethod
    def normalize_bank_guarantee_metadata(
            raw_bank_guarantee_metadata: list[BankGuaranteeEntity]
    ) -> list[BankGuaranteeEntity]:
        method_name = inspect.currentframe().f_code.co_name
        try:
            normalized_items: list[BankGuaranteeEntity] = []
            for item in raw_bank_guarantee_metadata:
                if item.file_name is None:
                    continue
                clean_name = item.file_name.removeprefix("cartas_fmv/").removesuffix(".pdf")
                new_item = BankGuaranteeEntity(
                    file_name=clean_name,
                    period_year=item.period_year,
                    period_month=item.period_month,
                    supervisory_record_id=item.supervisory_record_id,
                    type_document=item.type_document,
                    metadata=item.metadata,
                )
                normalized_items.append(new_item)
            return normalized_items
        except ValidationError as e:
            raise AnalyzeDataException(
                reason=AnalyzeDataErrorEnum.start_task_service,
                message=f"Existe un error crítico al normalizar la metadata en {method_name}"
            ) from e
