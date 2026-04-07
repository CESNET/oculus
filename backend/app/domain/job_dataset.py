import re
from enum import Enum

from .job_dataset_family import JobDatasetFamily


class JobDataset(Enum):
    SENTINEL1 = ("SENTINEL1", JobDatasetFamily.SENTINEL, "sentinel:feature_id")
    SENTINEL2 = ("SENTINEL2", JobDatasetFamily.SENTINEL, "sentinel:feature_id")
    # TODO vvv Landsaty rozlišovat třeba na 8, 9...
    LANDSAT = ("LANDSAT", JobDatasetFamily.LANDSAT, "landsat:display_id")  # TODO smazat a nechat jen L8, L9 apod.
    LANDSAT8 = ("LANDSAT8", JobDatasetFamily.LANDSAT, "landsat:display_id")  # TODO možná scene_id
    LANDSAT9 = ("LANDSAT9", JobDatasetFamily.LANDSAT, "landsat:display_id")  # TODO možná scene_id

    def __init__(self, dataset_name: str, family: JobDatasetFamily, product_key: str):
        self._dataset_name = dataset_name
        self._family = family
        self._product_key = product_key

    @property
    def family(self) -> JobDatasetFamily:
        return self._family

    @property
    def product_id_key(self) -> str:
        return self._product_key

    @classmethod
    def from_str(cls, name: str) -> "JobDataset":
        """
        Normalize input string and return corresponding JobDataset.
        Examples:
            "sentinel-1" -> JobDataset.SENTINEL1
            "SENTINEL1"  -> JobDataset.SENTINEL1
            "landsat8"   -> JobDataset.LANDSAT8
        """
        # normalize: upper, remove non-alphanum
        normalized = re.sub(r"[^A-Z0-9]", "", name.upper())
        for dataset in cls:
            if dataset._dataset_name == normalized:
                return dataset
        raise ValueError(f"Unknown dataset: {name}")


def get_dataset_family(dataset: JobDataset) -> JobDatasetFamily:
    return dataset.family
