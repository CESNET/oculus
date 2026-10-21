from dataclasses import dataclass
from pathlib import Path

from ..feature_state.output_format import OutputFormat
from ..feature_state.tile_group import TileGroup


@dataclass(frozen=True, slots=True)
class ProcessorOutput:
    visualization_id: str
    group: TileGroup
    format_name: OutputFormat
    path: Path
    zoom_levels: tuple[int, ...] = ()
