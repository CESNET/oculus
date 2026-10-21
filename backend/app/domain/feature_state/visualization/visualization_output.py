from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class VisualizationOutput:
    full_product: Path | None = None
    wm_tiles: Path | None = None
    wm_tiles_zoom_levels: list[int] = field(default_factory=list)

    def has_full_product(self) -> bool:
        return self.full_product is not None

    def has_wm_tiles(self) -> bool:
        return self.wm_tiles is not None

    def to_dict(self) -> dict:
        return {
            "full_product": (
                str(self.full_product)
                if self.full_product is not None
                else None
            ),
            "wm_tiles": (
                str(self.wm_tiles)
                if self.wm_tiles is not None
                else None
            ),
            "wm_tiles_zoom_levels": self.wm_tiles_zoom_levels,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VisualizationOutput":
        return cls(
            full_product=(
                Path(data["full_product"])
                if data.get("full_product")
                else None
            ),
            wm_tiles=(
                Path(data["wm_tiles"])
                if data.get("wm_tiles")
                else None
            ),
            wm_tiles_zoom_levels=data.get(
                "wm_tiles_zoom_levels",
                [],
            ),
        )
