import { useFiltersStore } from "../../../store/useFiltersStore";

/**
 * Datetime filter component
 * - Start & End date stacked vertically
 * - Prevents selecting future dates
 * - Uses YYYY-MM-DD format
 */
export default function DatetimeFilter() {
    const { datetime, setDatetime } = useFiltersStore();

    const today = new Date().toISOString().split("T")[0];

    const start = datetime.start?.slice(0, 10) ?? "";
    const end = datetime.end?.slice(0, 10) ?? "";

    const updateDate = (key: "start" | "end", value: string) => {
        if (!value) return;

        const selectedDate = new Date(value);
        const todayDate = new Date(today);

        if (selectedDate > todayDate) return;

        setDatetime({ [key]: value });
    };

    return (
        <div className="filter-section">
            <h3>Date Range</h3>

            <div className="date-stack">
                <div className="date-field">
                    <span className="date-label">Start</span>
                    <input
                        type="date"
                        value={start}
                        max={end || today}
                        onChange={(e) => updateDate("start", e.target.value)}
                    />
                </div>

                <div className="date-field">
                    <span className="date-label">End</span>
                    <input
                        type="date"
                        value={end}
                        min={start || undefined}
                        max={today}
                        onChange={(e) => updateDate("end", e.target.value)}
                    />
                </div>
            </div>
        </div>
    );
}