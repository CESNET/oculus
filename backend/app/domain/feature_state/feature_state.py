from pathlib import Path
from typing import Any, Optional


class FeatureStateId(str):
    @classmethod
    def from_parts(cls, dataset: str, feature_id: str) -> "FeatureStateId":
        return cls(f"{dataset}:{feature_id}")

    @property
    def dataset(self) -> str:
        return self.split(":", 1)[0]

    @property
    def feature_id(self) -> str:
        return self.split(":", 1)[1]


class FeatureState:
    def __init__(
            self,
            dataset: str,
            feature_id: str,

            feature_root_directory: Path | str,

            downloaded_files: Optional[list[dict[str, Any]]] = None,
    ):
        self.dataset = dataset
        self.feature_id = feature_id
        self.id = FeatureStateId.from_parts(dataset, feature_id)

        self.feature_root_directory = Path(feature_root_directory)

        self.downloaded_files = list(downloaded_files) if downloaded_files else []

    @classmethod
    def create(
            cls,
            dataset: str,
            feature_id: str,
            feature_root_directory: str,
    ) -> "FeatureState":
        feature_root_directory = Path(feature_root_directory) / dataset / feature_id

        return cls(
            dataset=dataset,
            feature_id=feature_id,
            feature_root_directory=feature_root_directory,
        )

    def serialize(self) -> dict:
        return {
            "_id": self.id,
            "dataset": self.dataset,
            "feature_id": self.feature_id,
            "feature_root_directory": str(self.feature_root_directory),
            "downloaded_files": self.downloaded_files,
        }

    @classmethod
    def deserialize(cls, data: dict) -> "FeatureState":
        obj = cls(
            dataset=data["dataset"],
            feature_id=data["feature_id"],
            feature_root_directory=data["feature_root_directory"],
            downloaded_files=data.get("downloaded_files", []),
        )

        obj.id = FeatureStateId(data["_id"])
        return obj

    def add_downloaded_files(self, new_files: list[str]) -> None:
        existing = set(self.downloaded_files)
        self.downloaded_files = list(existing.union(new_files))
