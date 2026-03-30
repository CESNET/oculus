import type { FiltersState } from "../store/useFiltersStore";

export const fetchFeaturesFromCDSE = async (
    filters: FiltersState,
    dataset: "S1" | "S2"
) => {
    const { bbox, datetime, sentinel1, sentinel2 } = filters;

    const polygon = `POLYGON((${bbox.west} ${bbox.north}, ${bbox.east} ${bbox.north}, ${bbox.east} ${bbox.south}, ${bbox.west} ${bbox.south}, ${bbox.west} ${bbox.north}))`;

    const parts: string[] = [];

    // 🌍 Spatial filter
    parts.push(
        `OData.CSC.Intersects(area=geography'SRID=4326;${polygon}')`
    );

    // 📦 Dataset-specific filters
    if (dataset === "S1") {
        if (sentinel1.productTypes.length) {
            const productTypeFilter = sentinel1.productTypes
                .map(
                    (p) =>
                        `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq '${p}')`
                )
                .join(" or ");

            parts.push(`(${productTypeFilter})`);
        }
    }

    if (dataset === "S2") {
        // kolekce
        parts.push(`Collection/Name eq 'SENTINEL-2'`);

        // productType (levels → S2MSI2A apod.)
        if (sentinel2.levels.length) {
            const productTypeFilter = sentinel2.levels
                .map(
                    (l) =>
                        `Attributes/OData.CSC.StringAttribute/any(att:att/Name eq 'productType' and att/OData.CSC.StringAttribute/Value eq 'S2MSI${l}')`
                )
                .join(" or ");

            parts.push(`(${productTypeFilter})`);
        }

        // cloud cover
        if (sentinel2.cloudCover != null) {
            parts.push(
                `Attributes/OData.CSC.DoubleAttribute/any(att:att/Name eq 'cloudCover' and att/OData.CSC.DoubleAttribute/Value le ${sentinel2.cloudCover})`
            );
        }

        // ❌ bandy jsme odstranili (API je takhle nepodporuje)
    }

    // ⏱ čas
    parts.push(
        `(ContentDate/Start ge ${datetime.start} and ContentDate/Start le ${datetime.end})`
    );

    // 🧠 finální složení
    const filterQuery = parts.join(" and ");

    const apiRootUrl =
        "https://catalogue.dataspace.copernicus.eu/odata/v1/Products";

    const endpoint = new URL(apiRootUrl);
    endpoint.searchParams.set("$filter", filterQuery);

    console.log("Endpoint URL:", endpoint.toString());

    const features: any[] = [];
    let url: string | null = endpoint.toString();

    while (url) {
        try {
            const resp = await fetch(url);
            const data = await resp.json();

            features.push(...data.value);

            if (!data["@odata.nextLink"] || features.length >= 5000) break;
            url = data["@odata.nextLink"];
        } catch (err) {
            console.error("CDSE fetch error", err);
            break;
        }
    }

    return features;
};