from abc import ABC, abstractmethod
from typing import Any


class BankGuaranteeMetadataRepository(ABC):
    @abstractmethod
    def get_collection_by_period(self, user_id: str, month: str, year: str) -> list[dict[str, Any]]:
        ...

    @abstractmethod
    def get_collection_by_ids(self, ids: list[str]) -> list[dict[str, Any]]:
        ...

    def get_collection_by_supervised_id_and_period(self, user_id: str, month: str, year: str) -> list[dict[str, Any]]:
        ...
