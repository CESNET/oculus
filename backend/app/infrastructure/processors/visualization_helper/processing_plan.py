from dataclasses import dataclass

from .visualization_task import VisualizationTask
from ....domain import (
    OutputFormat,
    TileGroup
)


@dataclass(frozen=True, slots=True)
class ProcessingPlan:
    visualizations: tuple[VisualizationTask, ...]
    outputs: dict[OutputFormat, set[TileGroup]]
