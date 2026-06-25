import logging
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class TileGroup(StrEnum):
    FULL_PRODUCT = "full_product"
    WM_TILES = "wm_tiles"


class OutputFormat(StrEnum):
    JPG = "jpg"
    PNG = "png"
    WEBP = "webp"


@dataclass(slots=True)
class ProcessedGroup:
    jpg: Path | None = None
    png: Path | None = None
    webp: Path | None = None

    def set_path(
            self,
            format_name: OutputFormat,
            path: Path,
    ) -> None:
        setattr(self, format_name.value, path)

    def get_path(
            self,
            format_name: OutputFormat,
    ) -> Path | None:
        return getattr(self, format_name.value)

    def is_processed(
            self,
            format_name: OutputFormat,
    ) -> bool:
        return self.get_path(format_name) is not None

    def to_dict(self) -> dict:
        return {
            "jpg": str(self.jpg) if self.jpg else None,
            "png": str(self.png) if self.png else None,
            "webp": str(self.webp) if self.webp else None,
        }

    @classmethod
    def from_dict(
            cls,
            data: dict,
    ) -> "ProcessedGroup":
        return cls(
            jpg=Path(data["jpg"]) if data.get("jpg") else None,
            png=Path(data["png"]) if data.get("png") else None,
            webp=Path(data["webp"]) if data.get("webp") else None,
        )


@dataclass(slots=True)
class FileState:
    filename: str
    download_path: Path | None = None

    full_product: ProcessedGroup = field(default_factory=ProcessedGroup)

    wm_tiles: ProcessedGroup = field(default_factory=ProcessedGroup)
    wm_tiles_zoom_levels: set[int] = field(default_factory=set)

    _logger: logging.Logger = logging.getLogger(__name__)

    @property
    def is_downloaded(self) -> bool:
        return self.download_path is not None

    def get_group(
            self,
            group: TileGroup,
    ) -> ProcessedGroup:
        return getattr(self, group.value)

    def set_processed_path(
            self,
            group: TileGroup,
            format_name: OutputFormat,
            path: Path,
    ) -> None:
        self.get_group(group).set_path(format_name=format_name, path=path)

    def set_wm_tiles_zoom_levels(self, zoom_levels: list[int]) -> None:
        print(f"Setting zoom levels for WebMercator tiles: {zoom_levels}")
        self.wm_tiles_zoom_levels = set(zoom_levels)

    def set_processed(
            self,
            group: TileGroup,
            format_name: OutputFormat,
            path: Path,
            zoom_levels: list[int] | None = None,
    ) -> None:
        if group == TileGroup.WM_TILES:
            if not self.wm_tiles_zoom_levels:
                if zoom_levels is None:
                    raise ValueError("Zoom levels must be provided when setting WebMercator tiles for the first time.")

                self.set_wm_tiles_zoom_levels(zoom_levels)

            elif zoom_levels is not None:
                self._logger.warning(
                    f"WebMercator zoom levels are already set to {sorted(self.wm_tiles_zoom_levels)}. "
                    f"Ignoring new zoom levels: {zoom_levels}."
                )

        self.set_processed_path(group=group, format_name=format_name, path=path)

    def get_processed_path(
            self,
            group: TileGroup,
            format_name: OutputFormat,
    ) -> Path | None:
        return self.get_group(group).get_path(format_name)

    def is_processed(
            self,
            group: TileGroup,
            format_name: OutputFormat,
    ) -> bool:
        return self.get_group(group).is_processed(format_name)

    def satisfies_outputs(self, outputs: dict) -> bool:
        for format_name, cfg in outputs.items():
            format = OutputFormat(format_name)

            if ((
                    cfg.get(TileGroup.FULL_PRODUCT.value, False)
            ) and not (
                    self.is_processed(TileGroup.FULL_PRODUCT, format)
            )):
                return False

            if ((
                    cfg.get(TileGroup.WM_TILES.value, False)
            ) and not (
                    self.is_processed(TileGroup.WM_TILES, format)
            )):
                return False

        return True

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "download_path": str(self.download_path) if self.download_path else None,
            TileGroup.FULL_PRODUCT.value: self.full_product.to_dict(),
            TileGroup.WM_TILES.value: self.wm_tiles.to_dict(),
            "wm_tiles_zoom_levels": self.wm_tiles_zoom_levels,
        }

    @classmethod
    def from_dict(
            cls,
            data: dict,
    ) -> "FileState":
        return cls(
            filename=data["filename"],
            download_path=Path(data["download_path"]) if data.get("download_path") else None,
            full_product=ProcessedGroup.from_dict(
                data.get(TileGroup.FULL_PRODUCT.value, {}),
            ),
            wm_tiles=ProcessedGroup.from_dict(
                data.get(TileGroup.WM_TILES.value, {}),
            ),
            wm_tiles_zoom_levels=set(
                data.get("wm_tiles_zoom_levels", [])
            ),
        )
