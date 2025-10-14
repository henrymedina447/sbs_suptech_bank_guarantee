import re
from rapidfuzz import fuzz

import unicodedata

from domain.contracts.compare_names_contract import CompareNamesContract

LEGAL_SUFFIXES = [
    r"S\.?A\.?C\.?", r"S\.?A\.?", r"S\.?R\.?L\.?", r"E\.?I\.?R\.?L\.?", r"S\.?A\.?A\.?", r"S\.?A\.?S\.?"
]
STOPWORDS = {"CONSTRUCTORA", "DE", "LA", "EL", "LOS", "LAS", "Y"}


class NamesAccuracyService:
    LEGAL_SUFFIXES = [
        r"S\.?A\.?C\.?", r"S\.?A\.?", r"S\.?R\.?L\.?", r"E\.?I\.?R\.?L\.?", r"S\.?A\.?A\.?", r"S\.?A\.?S\.?"
    ]
    STOPWORDS = {"CONSTRUCTORA", "DE", "LA", "EL", "LOS", "LAS", "Y"}

    @staticmethod
    def _strip_accents(s: str) -> str:
        nfkd = unicodedata.normalize("NFKD", s)
        return "".join(c for c in nfkd if not unicodedata.combining(c))

    @staticmethod
    def _normalize_company(name: str) -> str:
        s = NamesAccuracyService._strip_accents(name.upper())
        # Unifica separadores
        s = re.sub(r"[^\w\s]", " ", s)
        # Normaliza razones sociales (S.A.C. -> SAC, etc.)
        for suf in LEGAL_SUFFIXES:
            s = re.sub(rf"\b{suf}\b", " ", s)  # elimina la razón social
        # Quita stopwords frecuentes
        tokens = [t for t in s.split() if t and t not in STOPWORDS]
        # Colapsa espacios
        s = " ".join(tokens)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    @staticmethod
    def compare_names(a: str, b: str) -> CompareNamesContract:
        na, nb = NamesAccuracyService._normalize_company(a), NamesAccuracyService._normalize_company(b)
        return CompareNamesContract(
            norm_a=na,
            norm_b=nb,
            ratio=fuzz.ratio(na, nb),
            partial_ratio=fuzz.partial_ratio(na, nb),
            token_sort_ratio=fuzz.token_sort_ratio(na, nb),
            token_set_ratio=fuzz.token_set_ratio(na, nb),
        )
