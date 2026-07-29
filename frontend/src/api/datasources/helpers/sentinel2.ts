export function getSentinel2Platform(): string {
    return "Sentinel-2";
}

export function getSentinel2Satellite(name: string): string {
    if (name.startsWith("S2A")) {
        return "Sentinel-2A";
    }

    if (name.startsWith("S2B")) {
        return "Sentinel-2B";
    }

    return "Sentinel-2";
}

export function getSentinel2ProductType(name: string,): string | undefined {
    const match = name.match(/^S2[AB]_MSI(L1C|L2A)_/);

    return match?.[1];
}

export function getSentinel2Tile(name: string,): string | undefined {
    const match = name.match(/_T([A-Z0-9]{5})_/);

    return match?.[1];
}

export function getSentinel2ProcessingBaseline(name: string,): string | undefined {
    const match = name.match(/_N(\d{4})_/);

    return match?.[1];
}
