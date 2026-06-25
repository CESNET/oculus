from dataclasses import dataclass
from pathlib import Path

from ..feature_state.file_state import TileGroup, OutputFormat


@dataclass(slots=True, frozen=True)
class ProcessorOutput:
    source_file: str
    group: TileGroup
    format_name: OutputFormat
    path: Path
    zoom_levels: list[int] | None = None
