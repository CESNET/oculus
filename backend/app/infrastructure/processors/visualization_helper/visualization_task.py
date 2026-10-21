from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True, slots=True)
class VisualizationTask:
    id: str
    input_files: tuple[Path, ...]
    prefix: str | None = None
