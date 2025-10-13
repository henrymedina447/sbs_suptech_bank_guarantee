from abc import ABC, abstractmethod
from typing import Any


class InternalTablesRepository(ABC):

    @abstractmethod
    def get_collection(self, user_id: str, month: str, year: str) -> list[dict[str, Any]]:
        ...
