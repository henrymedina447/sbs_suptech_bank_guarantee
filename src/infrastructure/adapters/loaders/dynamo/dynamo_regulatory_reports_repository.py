from typing import Any

from domain.repositories.regulatory_report_repository import RegulatoryReportRepository


class DynamoRegulatoryReportsRepository(RegulatoryReportRepository):
    def get_collection(self, user_id: str, month: str, year: str) -> list[dict[str, Any]]:
        pass
