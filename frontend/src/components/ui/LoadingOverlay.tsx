import { useLoadingStore } from "../../store/useLoadingStore.ts";
import { Spinner, Button } from "react-bootstrap";
import "./LoadingOverlay.css";

export default function LoadingOverlay() {
    const { isLoading, stopLoading } = useLoadingStore();

    if (!isLoading) return null;

    return (
        <div className="loading-overlay">
            <Button
                variant="outline-light"
                className="close-button"
                onClick={stopLoading}
                title="Zrušit načítání"
            >
                ✕
            </Button>

            <div className="spinner-wrapper">
                <Spinner animation="border" variant="light" role="status" />
                <span className="loading-text">Please wait...</span>
            </div>
        </div>
    );
}