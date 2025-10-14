from pydantic import BaseModel


class CompareNamesContract(BaseModel):
    norm_a: str
    norm_b: str
    ratio: float
    partial_ratio: float
    token_sort_ratio: float
    token_set_ratio: float