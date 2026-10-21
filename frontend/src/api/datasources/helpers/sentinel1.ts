import type {Sentinel1Polarization} from "../../../types/visualization/sentinel1.ts";

export function getSentinel1Platform(): string {
    return "Sentinel-1";
}

export function getSentinel1Satellite(name: string): string {
    if (name.startsWith("S1A")) {
        return "Sentinel-1A";
    }

    if (name.startsWith("S1B")) {
        return "Sentinel-1B";
    }

    if (name.startsWith("S1C")) {
        return "Sentinel-1C";
    }

    if (name.startsWith("S1D")) {
        return "Sentinel-1D";
    }

    return "Sentinel-1";
}

export function getSentinel1ProductType(name: string): string | undefined {
    return name.split("_")[2];
}

const SENTINEL1_POLARIZATION_MAP: Record<
    string,
    Sentinel1Polarization[]
> = {
    DV: ["VV", "VH"],
    SV: ["VV"],
    DH: ["HH", "HV"],
    SH: ["HH"],
    VV: ["VV"],
    VH: ["VH"],
    HH: ["HH"],
    HV: ["HV"],
};

export function getSentinel1Polarizations(
    name: string,
): Sentinel1Polarization[] {
    const parts = name.split("_");
    const polarization = parts[3].slice(-2);

    const polarizations = SENTINEL1_POLARIZATION_MAP[polarization];

    if (!polarizations) {
        throw new Error(`Unknown polarization ${name}`);
    }

    return polarizations;
}

export function getSentinel1Title(name: string): string {
    const satellite = getSentinel1Satellite(name);

    const parts = name.split("_");

    const mode = parts[1];
    const product = parts[2];

    const polarizationLabel = getSentinel1Polarizations(name).join("/");

    return `${satellite} ${mode} ${product} (${polarizationLabel})`;
}
