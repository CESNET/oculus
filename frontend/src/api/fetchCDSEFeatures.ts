import type { FiltersState } from "../store/useFiltersStore";
import type { Feature } from "../store/useFeaturesStore";
import { Dataset } from "../types/datasets";
import { mapCDSEToFeature } from "./mappers/cdseMapper";

type CDSEProduct = {
    Id: string;
    Name: string;
    Collection?: { Name?: string };
    ContentDate?: { Start?: string };
    [key: string]: any;
};

type CDSEResponse = {
    value: CDSEProduct[];
    "@odata.nextLink"?: string;
};

const API_ROOT_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products";
const MAX_TOTAL_RESULTS = 5000;
const PAGE_SIZE = 1000;

/**
 * Hlavní funkce pro získání produktů z CDSE API.
 */
export const fetchCDSEFeatures = async (
    filters: FiltersState,
    dataset: Dataset,
    signal?: AbortSignal
): Promise<Feature[]> => {
    const filterQuery = buildCDSEQuery(filters, dataset);

    const endpoint = new URL(API_ROOT_URL);
    endpoint.searchParams.set("$filter", filterQuery);
    endpoint.searchParams.set("$top", PAGE_SIZE.toString());
    endpoint.searchParams.set("$orderby", "ContentDate/Start desc");

    let nextUrl: string | null = endpoint.toString();
    const allProducts: CDSEProduct[] = [];

    try {
        while (nextUrl && allProducts.length < MAX_TOTAL_RESULTS) {
            const response = await fetch(nextUrl, { signal });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`CDSE API error ${response.status}: ${errorText}`);
            }

            const data: CDSEResponse = await response.json();

            if (data.value && data.value.length > 0) {
                allProducts.push(...data.value);
            }

            nextUrl = data["@odata.nextLink"] || null;
        }
    } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') {
            return [];
        }
        console.error("Chyba při fetchování CDSE dat:", err);
        throw err;
    }

    return allProducts.slice(0, MAX_TOTAL_RESULTS).map(mapCDSEToFeature);
};

/** * Sestavení OData filtru s ošetřením Sentinel-1 specifik.
 */
const buildCDSEQuery = (filters: FiltersState, dataset: Dataset): string => {
    const { bbox, datetime, sentinel1, sentinel2 } = filters;
    const parts: string[] = [];

    // 1. Prostor (Longitude Latitude)
    const polygon = `POLYGON((${bbox.west} ${bbox.north}, ${bbox.east} ${bbox.north}, ${bbox.east} ${bbox.south}, ${bbox.west} ${bbox.south}, ${bbox.west} ${bbox.north}))`;
    parts.push(`OData.CSC.Intersects(area=geography'SRID=4326;${polygon}')`);

    // 2. Čas
    parts.push(`ContentDate/Start ge ${datetime.start} and ContentDate/Start le ${datetime.end}`);

    // 3. Dataset-specific
    if (dataset === Dataset.Sentinel1) {
        parts.push(`Collection/Name eq 'SENTINEL-1'`);

        // Product Types
        if (sentinel1.productTypes.length) {
            const sub = sentinel1.productTypes
                .map(p => `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '${p}')`)
                .join(" or ");
            parts.push(`(${sub})`);
        }

        // Processing Levels
        if (sentinel1.levels.length) {
            const sub = sentinel1.levels
                .map(l => `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingLevel' and att/OData.CSC.StringAttribute/Value eq 'LEVEL_${l}')`)
                .join(" or ");
            parts.push(`(${sub})`);
        }

        /**
         * 🚨 OPRAVA POLARIZACÍ (Kartézská expanze)
         * CDSE nezná 'VV' jako součást 'VV&VH' při použití 'eq'.
         * Musíme poslat všechny možné varianty řetězců, které se v API vyskytují.
         */
        if (sentinel1.polarizations.length) {
            const polMap: Record<string, string[]> = {
                'VV': ['VV', 'VV&VH', 'VV&VH&HH&HV'], // Přidány i vzácnější quad-pol varianty
                'VH': ['VH', 'VV&VH', 'VV&VH&HH&HV'],
                'HH': ['HH', 'HH&HV', 'VV&VH&HH&HV'],
                'HV': ['HV', 'HH&HV', 'VV&VH&HH&HV']
            };

            // Vytvoření unikátního seznamu všech API hodnot odpovídajících výběru uživatele
            const apiVariants = Array.from(new Set(
                sentinel1.polarizations.flatMap(p => polMap[p] || [p])
            ));

            const sub = apiVariants
                .map(v => `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'polarisationChannels' and att/OData.CSC.StringAttribute/Value eq '${v}')`)
                .join(" or ");
            parts.push(`(${sub})`);
        }
    }

    if (dataset === Dataset.Sentinel2) {
        parts.push(`Collection/Name eq 'SENTINEL-2'`);

        if (sentinel2.levels.length) {
            const sub = sentinel2.levels
                .map(l => `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI${l}')`)
                .join(" or ");
            parts.push(`(${sub})`);
        }

        if (sentinel2.cloudCover != null) {
            parts.push(`Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le ${sentinel2.cloudCover})`);
        }
    }

    return parts.join(" and ");
};
