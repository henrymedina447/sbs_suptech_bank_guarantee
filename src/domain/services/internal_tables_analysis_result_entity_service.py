from domain.models.entities.bank_guarantee_metadata_entity import BankGuaranteeEntity
from domain.models.entities.internal_tables_analysis_result_entity import InternalTablesAnalysisResultEntity
from domain.models.entities.internal_tables_entity import InternalTablesEntity


class InternalTablesAnalysisResultEntityService:

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
            BankGuaranteeEntity] = InternalTablesAnalysisResultEntityService._filter_metadata_by_origin_ccr(
            metadata=metadata,
            origin_ccr=origin_ccr,
        )
        total_ccr: float = InternalTablesAnalysisResultEntityService._sum_reduced_from_similar(similar_ccr)
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
        Calcula la diferencia del monto reducido de la tabla vs el monto reducido calculado de la tabla de
        metadatos
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
            origin_doc: InternalTablesEntity,
            metadata: list[BankGuaranteeEntity],
    ) -> InternalTablesAnalysisResultEntity:
        """

        :param origin_doc:
        :param metadata:
        :return:
        """
        reduced_amount: float = InternalTablesAnalysisResultEntityService._calculate_reduced_amount_from_values(
            origin_ccr=origin_doc.codigo_credito,
            metadata=metadata
        )
        difference_from_table: float = InternalTablesAnalysisResultEntityService.calculate_difference_from_table(
            origin_before_kco=origin_doc.saldo_mes_anterior,
            origin_actual_kco=origin_doc.saldo,
        )
        has_coincidence: bool = InternalTablesAnalysisResultEntityService.has_coincidence(
            difference_from_table,
            reduced_amount)
        return InternalTablesAnalysisResultEntity(
            ccr=origin_doc.codigo_credito,
            difference_from_table=str(difference_from_table),
            reduced_amount=str(reduced_amount),
            coincidence=has_coincidence
        )

    @staticmethod
    def _calculate_reduced_amount_from_values(origin_ccr: str, metadata: list[BankGuaranteeEntity]) -> float:
        similar_ccr: list[
            BankGuaranteeEntity] = InternalTablesAnalysisResultEntityService._filter_metadata_by_origin_ccr(
            metadata=metadata,
            origin_ccr=origin_ccr,
        )
        total_ccr: float = InternalTablesAnalysisResultEntityService._sum_reduced_from_values(similar_ccr)
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
