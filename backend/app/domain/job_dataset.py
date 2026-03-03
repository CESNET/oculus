from enum import Enum


class JobDataset(Enum):
    SENTINEL = "sentinel"
    LANDSAT = "landsat"
    OTHER = "other"
