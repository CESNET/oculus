from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class InputFileState:
    filename: str
    download_path: Path | None = None

    @property
    def is_downloaded(self) -> bool:
        return self.download_path is not None

    def to_dict(self) -> dict:
        return {
            "filename": self.filename,
            "download_path": (
                str(self.download_path)
                if self.download_path is not None
                else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "InputFileState":
        return cls(
            filename=data["filename"],
            download_path=(
                Path(data["download_path"])
                if data.get("download_path")
                else None
            ),
        )
