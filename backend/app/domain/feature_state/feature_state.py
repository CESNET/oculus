from __future__ import annotations

from pathlib import Path
from typing import Optional


class FeatureStateId(str):
    """
    Composite ID:
        dataset:feature_id
    """

    @classmethod
    def from_parts(
            cls,
            dataset: str,
            feature_id: str,
    ) -> "FeatureStateId":
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

            downloaded_files: Optional[list[str]] = None,
            processed_files: Optional[list[str]] = None,

            downloading_locks: Optional[dict] = None,
            processing_locks: Optional[dict] = None,
    ):
        self._dataset = dataset
        self._feature_id = feature_id

        self._id = FeatureStateId.from_parts(
            dataset=dataset,
            feature_id=feature_id,
        )

        self._feature_root_directory = Path(
            feature_root_directory
        )

        self._downloaded_files = downloaded_files or []
        self._processed_files = processed_files or []

        #
        # {
        #   "file.tif": {
        #       "job_id": "...",
        #       "reserved_at": datetime,
        #       "reserved_at_ts": float,
        #   }
        # }
        #
        self._downloading_locks = (
                downloading_locks or {}
        )

        self._processing_locks = (
                processing_locks or {}
        )

    # -------------------------
    # properties
    # -------------------------

    @property
    def id(self) -> FeatureStateId:
        return self._id

    @property
    def dataset(self) -> str:
        return self._dataset

    @property
    def feature_id(self) -> str:
        return self._feature_id

    @property
    def feature_root_directory(self) -> Path:
        return self._feature_root_directory

    @property
    def downloaded_files(self) -> list[str]:
        return self._downloaded_files

    @property
    def processed_files(self) -> list[str]:
        return self._processed_files

    @property
    def downloading_locks(self) -> dict:
        return self._downloading_locks

    @property
    def processing_locks(self) -> dict:
        return self._processing_locks

    # -------------------------
    # creation
    # -------------------------

    @classmethod
    def create(
            cls,
            dataset: str,
            feature_id: str,
            feature_root_directory: str,
    ) -> "FeatureState":
        resolved_path = Path(feature_root_directory) / dataset / feature_id

        return cls(
            dataset=dataset,
            feature_id=feature_id,
            feature_root_directory=resolved_path,
        )
