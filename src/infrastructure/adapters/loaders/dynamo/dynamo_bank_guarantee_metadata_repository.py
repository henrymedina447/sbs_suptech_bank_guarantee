from typing import Any

from domain.repositories.bank_guarantee_metadata_repository import BankGuaranteeMetadataRepository


class DynamoBankGuaranteeMetadataRepository(BankGuaranteeMetadataRepository):
    def get_collection_by_period(self, user_id: str, month: str, year: str) -> list[dict[str, Any]]:
        pass

    def get_collection_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        pass
