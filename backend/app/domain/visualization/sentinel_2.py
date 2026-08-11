import re
from dataclasses import dataclass
from enum import StrEnum


# ======================================================
# BANDS
# ======================================================

class Sentinel2Band(StrEnum):
    B1 = "1"
    B2 = "2"
    B3 = "3"
    B4 = "4"
    B5 = "5"
    B6 = "6"
    B7 = "7"
    B8 = "8"
    B8A = "8A"
    B9 = "9"
    B10 = "10"
    B11 = "11"
    B12 = "12"
    TCI = "TCI"


# ======================================================
# RGB
# ======================================================

@dataclass(frozen=True)
class Sentinel2RGBComposite:
    red: Sentinel2Band
    green: Sentinel2Band
    blue: Sentinel2Band


# ======================================================
# SPECTRAL INDEX
# ======================================================

@dataclass(frozen=True)
class Sentinel2SpectralIndex:
    expression: str
    required_bands: tuple[Sentinel2Band, ...]
    min: float | None = None
    max: float | None = None
    color_map: str | None = None


# ======================================================
# PRESETS
# ======================================================

class Sentinel2PresetType(StrEnum):
    RGB_COMPOSITE = "rgb-composite"
    SPECTRAL_INDEX = "spectral-index"


@dataclass(frozen=True)
class Sentinel2PresetBase:
    id: str
    label: str
    preset_type: Sentinel2PresetType


@dataclass(frozen=True)
class Sentinel2RGBPreset(Sentinel2PresetBase):
    composite: Sentinel2RGBComposite


@dataclass(frozen=True)
class Sentinel2SpectralIndexPreset(Sentinel2PresetBase):
    index: Sentinel2SpectralIndex


SENTINEL2_PRESETS = {
    "true-color": Sentinel2RGBPreset(
        id="true-color",
        label="True Color",
        preset_type=Sentinel2PresetType.RGB_COMPOSITE,
        composite=Sentinel2RGBComposite(
            red=Sentinel2Band.B4,
            green=Sentinel2Band.B3,
            blue=Sentinel2Band.B2,
        ),
    ),

    "false-color-infrared": Sentinel2RGBPreset(
        id="false-color-infrared",
        label="False Color Infrared",
        preset_type=Sentinel2PresetType.RGB_COMPOSITE,
        composite=Sentinel2RGBComposite(
            red=Sentinel2Band.B8,
            green=Sentinel2Band.B4,
            blue=Sentinel2Band.B3,
        ),
    ),

    "agriculture": Sentinel2RGBPreset(
        id="agriculture",
        label="Agriculture",
        preset_type=Sentinel2PresetType.RGB_COMPOSITE,
        composite=Sentinel2RGBComposite(
            red=Sentinel2Band.B11,
            green=Sentinel2Band.B8,
            blue=Sentinel2Band.B2,
        ),
    ),

    "geology": Sentinel2RGBPreset(
        id="geology",
        label="Geology",
        preset_type=Sentinel2PresetType.RGB_COMPOSITE,
        composite=Sentinel2RGBComposite(
            red=Sentinel2Band.B12,
            green=Sentinel2Band.B11,
            blue=Sentinel2Band.B2,
        ),
    ),
}


# ======================================================
# VISUALIZATION HELPERS
# ======================================================

def get_required_sentinel2_bands(
    visualizations: dict,
) -> set[Sentinel2Band]:
    required_bands: set[Sentinel2Band] = set()

    # Direct bands
    for band in visualizations.get("bands", []):
        try:
            required_bands.add(Sentinel2Band(band))
        except ValueError:
            continue

    # Custom RGB
    rgb = visualizations.get("rgb")

    if rgb:
        for channel in ("red", "green", "blue"):
            try:
                required_bands.add(Sentinel2Band(rgb[channel]))
            except (KeyError, ValueError):
                continue

    # Presets
    for preset_id in visualizations.get("presets", []):
        preset = SENTINEL2_PRESETS.get(preset_id)

        if preset is None:
            continue

        if isinstance(preset, Sentinel2RGBPreset):
            required_bands.update({
                preset.composite.red,
                preset.composite.green,
                preset.composite.blue,
            })

        elif isinstance(preset, Sentinel2SpectralIndexPreset):
            required_bands.update(preset.index.required_bands)

    return required_bands


def filter_sentinel2_files(
    files: list[str],
    visualizations: dict,
) -> list[str]:
    if not files:
        return []

    required_bands = get_required_sentinel2_bands(visualizations)

    if not required_bands:
        return files

    filtered_files: list[str] = []

    for file in files:
        filename = file.split("/")[-1]
        filename_parts = re.split(r"[_.]", filename)

        if not any(
            band.value in filename_parts
            for band in required_bands
        ):
            continue

        filtered_files.append(file)

    return filtered_files
