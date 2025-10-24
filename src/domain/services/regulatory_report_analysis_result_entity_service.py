import logging

from domain.contracts.compare_names_contract import CompareNamesContract
from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.fmv_guarantee_letters_result_entity import FMVGuaranteeLettersResultEntity
from domain.models.entities.regulatory_report_analysis_result_entity import RegulatoryReportAnalysisResultEntity
from domain.models.entities.regulatory_report_entity import RegulatoryReportEntity
from domain.services.names_accuracy_service import NamesAccuracyService

logger = logging.getLogger("app.workflows")


class RegulatoryReportAnalysisResultEntityService:

    @staticmethod
    def calculate_reduced_amount(origin_ccr: str, metadata: list[BankGuaranteeEntity]) -> float:
        """
        Calcula el monto reducido buscando todos los documentos que tengan como nombre el mismo código de
        crédito y sumando los campos de "disminuido"
        :param origin_ccr: Código de crédito de la tabla de reporte
        :param metadata: Lista de todos los metadatos disponibles
        :return:
        """
        similar_ccr: list[
            BankGuaranteeEntity] = RegulatoryReportAnalysisResultEntityService._filter_metadata_by_origin_ccr(
            metadata=metadata,
            origin_ccr=origin_ccr,
        )
        total_ccr: float = RegulatoryReportAnalysisResultEntityService._sum_reduced_from_similar(similar_ccr)
        return total_ccr

    @staticmethod
    def _sum_reduced_from_similar(similar_ccr: list[BankGuaranteeEntity]) -> float:
        """
        Dada una lista de elementos de metadata, suma todos los campos reduced amount y retorna el total
        :param similar_ccr:
        :return:
        """
        total = 0.0
        for s in similar_ccr:
            total += float(s.metadata.reduced_amount if s.metadata.reduced_amount else 0)
        return total

    @staticmethod
    def _filter_metadata_by_origin_ccr(
            origin_ccr: str,
            metadata: list[BankGuaranteeEntity]
    ) -> list[BankGuaranteeEntity]:
        """
        Dado un código de crédito, busca todos los file_names que tengan el mismo código de crédito
        :param origin_ccr:
        :param metadata:
        :return:
        """
        similar_ccr: list[BankGuaranteeEntity] = []
        for m in metadata:
            if m.file_name is None:
                continue
            if origin_ccr in m.file_name:
                similar_ccr.append(m)
        return similar_ccr

    @staticmethod
    def calculate_difference_from_table(
            origin_before_kco: float | None,
            origin_actual_kco: float | None,
    ) -> float:
        """
        Calcula la diferencia existente en la tabla del saldo actual y el saldo anterior
        :param origin_before_kco: valor preliminar de la tabla de reporte
        :param origin_actual_kco: valor actual de la tabla de reporte
        :return:
        """
        aux_1: float = float(origin_before_kco if origin_before_kco is not None else 0)
        aux_2: float = float(origin_actual_kco if origin_actual_kco is not None else 0)
        return aux_2 - aux_1

    @staticmethod
    def has_coincidence(difference: float, reduced_amount: float) -> bool:
        """
        Evalúa si existe una diferencia entre el monto reducido de la tabla de reporte y el de la metadata
        :param reduced_amount: Diferencia calculada desde los metadatos
        :param difference: Diferencia calculada con los datos de la tabla
        :return:
        """
        return difference == reduced_amount

    @staticmethod
    def get_analyzed_reduced_amount_item(
            origin_doc: RegulatoryReportEntity,
            metadata: list[BankGuaranteeEntity]
    ) -> RegulatoryReportAnalysisResultEntity:
        """
        Calcula el item del análisis del reporte respecto al monto reducido
        :param origin_doc:
        :param metadata: Todos los elementos de la metadata disponibles
        :return:
        """
        reduced_amount: float = RegulatoryReportAnalysisResultEntityService._calculate_reduced_amount_from_values(
            origin_ccr=origin_doc.ccr,
            metadata=metadata
        )
        difference_from_table: float = RegulatoryReportAnalysisResultEntityService.calculate_difference_from_table(
            origin_before_kco=origin_doc.kco_mes_anterior,
            origin_actual_kco=origin_doc.kco,
        )
        has_coincidence: bool = RegulatoryReportAnalysisResultEntityService.has_coincidence(
            difference_from_table,
            reduced_amount
        )
        return RegulatoryReportAnalysisResultEntity(
            ccr=origin_doc.ccr,
            difference_from_table=str(difference_from_table),
            reduced_amount=str(reduced_amount),
            coincidence=has_coincidence
        )

    @staticmethod
    def _calculate_reduced_amount_from_values(origin_ccr: str, metadata: list[BankGuaranteeEntity]) -> float:
        similar_ccr: list[
            BankGuaranteeEntity] = RegulatoryReportAnalysisResultEntityService._filter_metadata_by_origin_ccr(
            metadata=metadata,
            origin_ccr=origin_ccr,
        )
        total_ccr: float = RegulatoryReportAnalysisResultEntityService._sum_reduced_from_values(similar_ccr)
        return total_ccr

    @staticmethod
    def _sum_reduced_from_values(
            similar_ccr: list[BankGuaranteeEntity]) -> float:
        """
        Calcular el valor reducido haciendo la diferencia entre el valor total menos el valor
        desembolsado
        :param similar_ccr: Contiene los elementos asociados a la carta
        :return:
        """
        total = 0.0
        for s in similar_ccr:
            partial_total = float(s.metadata.total_amount if s.metadata.total_amount else 0)
            partial_disbursement = float(s.metadata.disbursed_amount if s.metadata.disbursed_amount else 0)
            partial_result = partial_total - partial_disbursement
            total += partial_result
        return total

    @staticmethod
    def get_analyze_fmv_guarantee_letters_item(
            origin_doc: RegulatoryReportEntity,
            metadata: list[BankGuaranteeEntity]
    ) -> list[FMVGuaranteeLettersResultEntity]:
        try:
            similar = RegulatoryReportAnalysisResultEntityService._filter_metadata_by_origin_ccr(
                origin_ccr=origin_doc.ccr,
                metadata=metadata
            )
            total: list[FMVGuaranteeLettersResultEntity] = []
            client_origin: str = origin_doc.ncl
            for s in similar:
                accuracy = RegulatoryReportAnalysisResultEntityService.calculate_coincidence(
                    client_origin=client_origin,
                    client_metadata=s.metadata.promotor
                )
                aux: FMVGuaranteeLettersResultEntity = FMVGuaranteeLettersResultEntity(
                    ccr=origin_doc.ccr,
                    letter_text=s.metadata.letter_text,
                    client_origin=client_origin,
                    client_metadata=s.metadata.promotor,
                    coincidence=accuracy > 85

                )
                total.append(aux)
            return total
        except Exception as e:
            logger.error(f"error: {str(e)}")
            return []

    @staticmethod
    def calculate_coincidence(client_origin: str, client_metadata: str) -> float:
        comparisons: CompareNamesContract = NamesAccuracyService.compare_names(
            client_origin,
            client_metadata
        )
        return comparisons.token_set_ratio
