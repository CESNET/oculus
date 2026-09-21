from enum import StrEnum


# ======================================================
# POLARIZATIONS
# ======================================================

class Sentinel1Polarization(StrEnum):
    HH = "HH"
    HV = "HV"
    VV = "VV"
    VH = "VH"
