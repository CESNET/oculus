const API_ROOT_URL =    "https://catalogue.dataspace.copernicus.eu/odata/v1/Products";

const MAX_TOTAL_RESULTS = 5000;
const PAGE_SIZE = 1000;

export async function fetchProducts(
    filter: string,
    signal?: AbortSignal,
): Promise<any[]> {
    const endpoint = new URL(API_ROOT_URL);

    endpoint.searchParams.set("$filter", filter);
    endpoint.searchParams.set("$top", PAGE_SIZE.toString());
    endpoint.searchParams.set(
        "$orderby",
        "ContentDate/Start desc",
    );

    let nextUrl: string | null = endpoint.toString();

    const products: any[] = [];

    try {
        while (nextUrl && products.length < MAX_TOTAL_RESULTS) {
            const response = await fetch(nextUrl, {
                signal,
            });

            if (!response.ok) {
                const error = await response.text();

                throw new Error(
                    `CDSE API returned ${response.status}: ${error}`,
                );
            }

            const json = await response.json();

            if (Array.isArray(json.value)) {
                products.push(...json.value);
            }

            nextUrl = json["@odata.nextLink"] ?? null;
        }

        return products.slice(0, MAX_TOTAL_RESULTS);
    } catch (err) {
        if (
            err instanceof Error &&
            err.name === "AbortError"
        ) {
            return [];
        }

        throw err;
    }
}
