export const parseWKTToCoordinates = (wkt: string,): [number, number][] => {
    try {
        const match = wkt.match(/\(\((.*)\)\)/);

        if (!match) {
            return [];
        }

        return match[1].split(",").map((point) => {
            const [lng, lat] = point.trim().split(/\s+/).map(Number);

            return [lat, lng];
        });
    } catch {
        return [];
    }
};
