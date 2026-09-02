from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .input_file_state import InputFileState
from .visualization import VisualizationState


@dataclass(frozen=True, slots=True)
class FeatureStateId:
    dataset: str
    feature_id: str

    def __str__(self) -> str:
        return f"{self.dataset}:{self.feature_id}"

    @classmethod
    def parse(cls, value: str) -> "FeatureStateId":
        dataset, feature_id = value.split(":", 1)

        return cls(
            dataset=dataset,
            feature_id=feature_id,
        )


@dataclass(slots=True)
class FeatureState:
    id: FeatureStateId
    feature_root_directory: Path

    input_files: dict[str, InputFileState] = field(default_factory=dict)
    visualizations: dict[str, VisualizationState] = field(default_factory=dict)

    @property
    def dataset(self) -> str:
        return self.id.dataset

    @property
    def feature_id(self) -> str:
        return self.id.feature_id

    # -------------------------
    # input files
    # -------------------------

    def get_file(
            self,
            filename: str,
    ) -> InputFileState | None:
        return self.input_files.get(filename)

    def get_or_create_file(
            self,
            filename: str,
    ) -> InputFileState:
        file_state = self.input_files.get(filename)

        if file_state is None:
            file_state = InputFileState(
                filename=filename
            )
            self.input_files[filename] = file_state

        return file_state

    def is_file_downloaded(
            self,
            filename: str,
    ) -> bool:
        file_state = self.input_files.get(filename)

        return (
                file_state is not None
                and file_state.is_downloaded
        )

    # -------------------------
    # visualizations
    # -------------------------

    def get_visualization(
            self,
            visualization_id: str,
    ) -> VisualizationState | None:
        return self.visualizations.get(visualization_id)

    def get_or_create_visualization(
            self,
            visualization_id: str,
    ) -> VisualizationState:
        visualization = self.visualizations.get(visualization_id)

        if visualization is None:
            visualization = VisualizationState()
            self.visualizations[visualization_id] = visualization

        return visualization

    # -------------------------
    # serialization
    # -------------------------

    def to_dict(self) -> dict:
        return {
            "dataset": self.id.dataset,
            "feature_id": self.id.feature_id,
            "feature_root_directory": str(self.feature_root_directory),

            "input_files": [
                input_file_state.to_dict()
                for input_file_state in self.input_files.values()
            ],

            "visualizations": {
                visualization_id: state.to_dict()
                for visualization_id, state
                in self.visualizations.items()
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FeatureState":
        return cls(
            id=FeatureStateId(
                dataset=data["dataset"],
                feature_id=data["feature_id"],
            ),
            feature_root_directory=Path(data["feature_root_directory"]),
            input_files={
                input_file_state["filename"]: InputFileState.from_dict(input_file_state)
                for input_file_state
                in data.get("input_files", [])
            },
            visualizations={
                visualization_id: VisualizationState.from_dict(visualization_state)
                for visualization_id, visualization_state
                in data.get("visualizations", {}).items()
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
