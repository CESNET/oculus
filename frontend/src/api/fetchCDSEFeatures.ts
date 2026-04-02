import type {FiltersState} from "../store/useFiltersStore";
import type {Feature} from "../store/useFeaturesStore";
import {Dataset} from "../types/datasets";
import {mapCDSEToFeature} from "./mappers/cdseFeatureMapper.ts";

const API_ROOT_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products";
const MAX_TOTAL_RESULTS = 5000;
const PAGE_SIZE = 1000;

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
    const allProducts: any[] = [];

    try {
        while (nextUrl && allProducts.length < MAX_TOTAL_RESULTS) {
            const response = await fetch(nextUrl, {signal});
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`CDSE API error ${response.status}: ${errorText}`);
            }

            const data = await response.json();
            if (data.value) allProducts.push(...data.value);
            nextUrl = data["@odata.nextLink"] || null;
        }
    } catch (err) {
        if (err instanceof Error && err.name === 'AbortError') return [];
        throw err;
    }

    return allProducts
        .slice(0, MAX_TOTAL_RESULTS)
        .map(item => mapCDSEToFeature(item, dataset));
};

const buildCDSEQuery = (filters: FiltersState, dataset: Dataset): string => {
    const { bbox, datetime, sentinel1, sentinel2 } = filters;
    const parts: string[] = [];

    // 1. Spatial
    const polygon = `POLYGON((${bbox.west} ${bbox.north}, ${bbox.east} ${bbox.north}, ${bbox.east} ${bbox.south}, ${bbox.west} ${bbox.south}, ${bbox.west} ${bbox.north}))`;
    parts.push(`OData.CSC.Intersects(area=geography'SRID=4326;${polygon}')`);

    // 2. Time - Ujisti se, že datetime.start/end jsou ISO stringy
    const timeStart = new Date(datetime.start).toISOString();
    const timeEnd = new Date(datetime.end).toISOString();
    parts.push(`ContentDate/Start ge ${timeStart} and ContentDate/Start le ${timeEnd}`);

    // 3. Dataset Specifics
    if (dataset === Dataset.Sentinel1) {
        console.log("Sentinel-1: ", sentinel1);
        parts.push(`Collection/Name eq 'SENTINEL-1'`);

        // Operational Mode (v původním kódu sensingTypesApiCall)
        // Pozor: v TS ti chyběl filtr na operationalMode, který v JS byl
        if (sentinel1.sensingTypes && sentinel1.sensingTypes.length) {
            const sub = sentinel1.sensingTypes.map(t =>
                `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'operationalMode' and att/OData.CSC.StringAttribute/Value eq '${t}')`
            ).join(" or ");
            parts.push(`(${sub})`);
        }

        if (sentinel1.productTypes.length) {
            const sub = sentinel1.productTypes.map(p =>
                `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '${p}')`
            ).join(" or ");
            parts.push(`(${sub})`);
        }

        if (sentinel1.levels.length) {
            const sub = sentinel1.levels.map(l =>
                `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'processingLevel' and att/OData.CSC.StringAttribute/Value eq 'LEVEL${l}')`
            ).join(" or ");
            parts.push(`(${sub})`);
        }

        if (sentinel1.polarizations.length) {
            const polMap: Record<string, string[]> = {
                'VV': ['VV', 'VV&VH'],
                'VH': ['VH', 'VV&VH'],
                'HH': ['HH', 'HH&HV'],
                'HV': ['HV', 'HH&HV']
            };
            const variants = Array.from(new Set(sentinel1.polarizations.flatMap(p => polMap[p] || [p])));

            const sub = variants.map(v => {
                return `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'polarisationChannels' and att/OData.CSC.StringAttribute/Value eq '${v}')`;
            }).join(" or ");
            parts.push(`(${sub})`);
        }
    }

    if (dataset === Dataset.Sentinel2) {
        parts.push(`Collection/Name eq 'SENTINEL-2'`);
        if (sentinel2.levels.length) {
            const sub = sentinel2.levels.map(l => `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI${l}')`).join(" or ");
            parts.push(`(${sub})`);
        }
        if (sentinel2.cloudCover != null) {
            parts.push(`Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le ${sentinel2.cloudCover.toFixed(2)})`);
        }
    }

    return parts.join(" and ");
};