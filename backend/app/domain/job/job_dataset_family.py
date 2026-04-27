from enum import Enum


class JobDatasetFamily(Enum):
    SENTINEL = "sentinel"
    LANDSAT = "landsat"

    def __str__(self) -> str:
        return self.value
