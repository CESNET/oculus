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

export function getSentinel1Title(name: string): string {
    const satellite = getSentinel1Satellite(name);

    const parts = name.split("_");

    const mode = parts[1]; // IW
    const product = parts[2]; // GRDH
    const polarization = parts[3].slice(-2); // DV/SV/DH/SH

    const polarizationLabel = {
        DV: "VV/VH",
        SV: "VV",
        DH: "HH/VH",
        SH: "HH",
    }[polarization] ?? polarization;

    return `${satellite} ${mode} ${product} (${polarizationLabel})`;
}
