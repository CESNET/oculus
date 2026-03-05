from enum import Enum


class JobDataset(Enum):
    SENTINEL = "sentinel"
    LANDSAT = "landsat"

    def product_id_key(self) -> str:
        mapping = {
            JobDataset.SENTINEL: "sentinel:feature_id",
            JobDataset.LANDSAT: "landsat:display_id", # TODO možná scene_id
        }

        if self not in mapping:
            raise ValueError(f"Unsupported dataset: {self}")

        return mapping[self]
