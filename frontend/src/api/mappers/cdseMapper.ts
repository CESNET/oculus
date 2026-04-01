import type { Feature } from "../../store/useFeaturesStore";

export const mapCDSEToFeature = (item: any): Feature => {
    return {
        id: item.Id,
        title: item.Name,
        platform: item.Collection?.Name ?? "Unknown",
        acquisitionDate: item.ContentDate?.Start ?? "",
        productUrl: item["__metadata"]?.uri ?? "", // fallback
    };
};