import {useLoadingStore} from "../../store/useLoadingStore";
import {LoadingType} from "../../types/loadingTypes";
import "./LoadingOverlay.css";


const loadingMessages: Record<
    LoadingType,
    { title: string; description: string }
> = {
    [LoadingType.DEFAULT]: {
        title: "Working...",
        description: "Please wait a moment",
    },
    [LoadingType.FETCH_FEATURES]: {
        title: "Fetching satellite data",
        description: "Searching the metadata catalogue for matching products",
    },
    [LoadingType.VISUALIZING]: {
        title: "Visualizing satellite data",
        description: "Executing visualization of satellite products",
    },
    [LoadingType.DOWNLOADING]: {
        title: "Downloading satellite data",
        description: "Retrieving the required satellite products",
    },
    [LoadingType.PROCESSING]: {
        title: "Processing satellite data",
        description: "Preparing your satellite imagery",
    },
};

export default function LoadingOverlay() {
    const isLoading = useLoadingStore((state) => state.isLoading);
    const loadingType = useLoadingStore((state) => state.loadingType);
    const stopLoading = useLoadingStore((state) => state.stopLoading);

    if (!isLoading) return null;

    const message = loadingMessages[loadingType];

    return (
        <div className="loading-overlay">
            <div
                className="loading-content"
                role="status"
                aria-live="polite"
            >
                <div className="loading-indicator" aria-hidden="true">
                    <span className="loading-orbit loading-orbit-one" />
                    <span className="loading-orbit loading-orbit-two" />
                    <span className="loading-orbit loading-orbit-three" />
                    <span className="loading-core" />
                </div>

                <div className="loading-title">
                    {message.title}
                </div>

                <div className="loading-description">
                    {message.description}
                </div>

                <button
                    type="button"
                    className="loading-cancel"
                    onClick={stopLoading}
                >
                    <span aria-hidden="true">×</span>
                    Cancel
                </button>
            </div>
        </div>
    );
}
