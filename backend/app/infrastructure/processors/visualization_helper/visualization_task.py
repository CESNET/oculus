from dataclasses import dataclass
from pathlib import Path



@dataclass(frozen=True, slots=True)
class VisualizationTask:
    """
    Processing task for a single visualization.

    The task ID identifies the visualization and corresponds
    to the key in FeatureState.visualizations.

    input_files contains the concrete local input files required
    to create the visualization.
    """

    id: str
    input_files: tuple[Path, ...]
