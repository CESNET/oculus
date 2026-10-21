export function getSentinel2Platform(): string {
    return "Sentinel-2";
}

export function getSentinel2Satellite(name: string): string {
    if (name.startsWith("S2A")) {
        return `${getSentinel2Platform()}A`;
    }

    if (name.startsWith("S2B")) {
        return `${getSentinel2Platform()}B`;
    }

    if (name.startsWith("S2C")) {
        return `${getSentinel2Platform()}C`;
    }

    return getSentinel2Platform();
}

export function getSentinel2ProductType(name: string,): string | undefined {
    const match = name.match(/^S2[ABC]_MSI(L1C|L2A)_/);

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
