from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class FileState:
    filename: str
    download_path: Path | None = None
    processed_path: list[Path] | None = None

    @property
    def is_downloaded(self) -> bool:
        return self.download_path is not None

    @property
    def is_processed(self) -> bool:
        return self.processed_path is not None

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "download_path": str(self.download_path) if self.download_path else None,
            "processed_path": str(self.processed_path) if self.processed_path else None,
        }

    @classmethod
    def from_dict(
            cls,
            data: dict,
    ) -> "FileState":
        return cls(
            filename=data["filename"],
            download_path=Path(data["download_path"]) if data.get("download_path") else None,
            processed_path=Path(data["processed_path"]) if data.get("processed_path") else None
        )


@dataclass(frozen=True, slots=True)
class FeatureStateId:
    dataset: str
    feature_id: str

    def __str__(self) -> str:
        return f"{self.dataset}:{self.feature_id}"

    @classmethod
    def parse(
            cls,
            value: str,
    ) -> "FeatureStateId":
        dataset, feature_id = value.split(":", 1, )
        return cls(
            dataset=dataset,
            feature_id=feature_id,
        )


@dataclass(frozen=True, slots=True)
class FeatureState:
    id: FeatureStateId
    feature_root_directory: Path
    files: dict[str, FileState] = field(default_factory=dict)

    # -------------------------
    # convenience
    # -------------------------

    @property
    def dataset(self) -> str:
        return self.id.dataset

    @property
    def feature_id(self) -> str:
        return self.id.feature_id

    # -------------------------
    # file operations
    # -------------------------

    def _get_or_create_file_state(self, file: str) -> FileState:
        state = self.files.get(file)
        if state is None:
            state = FileState(filename=file)
            self.files[file] = state
        return state

    def get_file_state(
            self,
            file: str,
    ) -> FileState | None:
        return self.files.get(file)

    def set_file_processed_path(
            self,
            file: str,
            path: Path,
    ) -> None:
        self._get_or_create_file_state(file).processed_path = path

    def is_file_downloaded(
            self,
            file: str,
    ) -> bool:
        state = self.files.get(file)
        return state is not None and state.is_downloaded

    def is_file_processed(
            self,
            filename: str,
    ) -> bool:
        state = self.files.get(filename)
        return state is not None and state.is_processed

    @property
    def downloaded_files(self) -> list[str]:
        return [
            filename
            for filename, state in self.files.items()
            if state.is_downloaded
        ]

    @property
    def processed_files(self) -> list[str]:
        return [
            filename
            for filename, state in self.files.items()
            if state.is_processed
        ]

    # -------------------------
    # serialization
    # -------------------------

    def to_dict(self) -> dict:
        return {
            "dataset": self.dataset,
            "feature_id": self.feature_id,
            "feature_root_directory": str(self.feature_root_directory),
            "files": [
                state.to_dict()
                for state in self.files.values()
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FeatureState":
        files_list = data.get("files", [])

        return cls(
            id=FeatureStateId(
                dataset=data["dataset"],
                feature_id=data["feature_id"],
            ),
            feature_root_directory=Path(data["feature_root_directory"]),
            files={
                item["filename"]: FileState.from_dict(item)
                for item in files_list
            },
        )

    # -------------------------
    # factory
    # -------------------------

    @classmethod
    def create(
            cls,
            dataset: str,
            feature_id: str,
            root_directory: str | Path,
    ) -> "FeatureState":
        return cls(
            id=FeatureStateId(
                dataset=dataset,
                feature_id=feature_id,
            ),
            feature_root_directory=Path(root_directory) / dataset / feature_id,
        )
