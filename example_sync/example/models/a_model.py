"""Define a simple Model data type."""

from typing import List

from db_wrapper.model import ModelData


class AModel(ModelData):
    """An example Item."""

    string: str
    integer: int
    array: List[str]
