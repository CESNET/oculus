from dataclasses import dataclass
from enum import StrEnum


# ======================================================
# BANDS
# ======================================================

class Sentinel2Band(StrEnum):
    B1 = "B01"
    B2 = "B02"
    B3 = "B03"
    B4 = "B04"
    B5 = "B05"
    B6 = "B06"
    B7 = "B07"
    B8 = "B08"
    B8A = "B8A"
    B9 = "B09"
    B10 = "B10"
    B11 = "B11"
    B12 = "B12"
    TCI = "TCI"


# ======================================================
# RGB
# ======================================================

@dataclass(frozen=True, slots=True)
class Sentinel2RGBComposite:
    red: Sentinel2Band
    green: Sentinel2Band
    blue: Sentinel2Band


# ======================================================
# INDEXES
# ======================================================

class Sentinel2Index(StrEnum):
    HONS = "HONS"
    NDVI = "NDVI"
    NDWI = "NDWI"
    NDMI = "NDMI"
    NDSI = "NDSI"
    ND_UNSPEC = "ND_UNSPEC"


# Band order is aligned with GJTIFF input.
SENTINEL2_INDEX_BANDS: dict[Sentinel2Index, tuple[Sentinel2Band, ...]] = {
    Sentinel2Index.HONS: (
        Sentinel2Band.B4,
        Sentinel2Band.B3,
        Sentinel2Band.B2,
    ),

    Sentinel2Index.NDVI: (
        Sentinel2Band.B8,
        Sentinel2Band.B4,
    ),

    Sentinel2Index.NDWI: (
        Sentinel2Band.B3,
        Sentinel2Band.B8,
    ),

    Sentinel2Index.NDMI: (
        Sentinel2Band.B8A,
        Sentinel2Band.B11,
    ),

    Sentinel2Index.NDSI: (
        Sentinel2Band.B3,
        Sentinel2Band.B11,
        Sentinel2Band.B4,
        Sentinel2Band.B2,
    ),
}


# ======================================================
# PRESETS
# ======================================================

class Sentinel2PresetType(StrEnum):
    RGB_COMPOSITE = "rgb-composite"
    INDEX = "index"


@dataclass(frozen=True, slots=True)
class Sentinel2PresetBase:
    id: str
    label: str
    preset_type: Sentinel2PresetType


@dataclass(frozen=True, slots=True)
class Sentinel2RGBPreset(Sentinel2PresetBase):
    composite: Sentinel2RGBComposite


@dataclass(frozen=True, slots=True)
class Sentinel2IndexPreset(Sentinel2PresetBase):
    index: Sentinel2Index


SENTINEL2_PRESETS = {
    # ======================================================
    # RGB PRESETS
    # ======================================================

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

    # ======================================================
    # INDEX PRESETS
    # ======================================================

    "hons": Sentinel2IndexPreset(
        id="hons",
        label="HONS",
        preset_type=Sentinel2PresetType.INDEX,
        index=Sentinel2Index.HONS,
    ),

    "ndvi": Sentinel2IndexPreset(
        id="ndvi",
        label="NDVI",
        preset_type=Sentinel2PresetType.INDEX,
        index=Sentinel2Index.NDVI,
    ),

    "ndwi": Sentinel2IndexPreset(
        id="ndwi",
        label="NDWI",
        preset_type=Sentinel2PresetType.INDEX,
        index=Sentinel2Index.NDWI,
    ),

    "ndmi": Sentinel2IndexPreset(
        id="ndmi",
        label="NDMI",
        preset_type=Sentinel2PresetType.INDEX,
        index=Sentinel2Index.NDMI,
    ),

    "ndsi": Sentinel2IndexPreset(
        id="ndsi",
        label="NDSI",
        preset_type=Sentinel2PresetType.INDEX,
        index=Sentinel2Index.NDSI,
    ),
}


# ======================================================
# DOMAIN HELPERS
# ======================================================

def get_required_sentinel2_bands(
        visualizations: dict,
) -> set[Sentinel2Band]:
    """
    Return all Sentinel-2 bands required by a visualization request.
    """

    required_bands: set[Sentinel2Band] = set()

    # Single bands
    for band in visualizations.get("bands", []):
        try:
            required_bands.add(Sentinel2Band(band))
        except ValueError:
            continue

    # Custom RGB composite
    rgb = visualizations.get("rgb_composite")

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

        elif isinstance(preset, Sentinel2IndexPreset):
            required_bands.update(
                SENTINEL2_INDEX_BANDS[preset.index]
            )

    return required_bands
