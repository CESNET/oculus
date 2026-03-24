import { useState } from "react";
import FiltersPanel from "./FiltersPanel";
import FeaturesPanel from "./FeaturesPanel";
import VisualizationPanel from "./VisualizationPanel";
import "./Sidebar.css";

const tabs = ["Filters", "Features", "Visualization"];

export default function Sidebar() {
    const [activeTab, setActiveTab] = useState(0);

    return (
        <div className="sidebar">
            <div className="sidebar-tabs">
                {tabs.map((tab, i) => (
                    <button
                        key={tab}
                        className={activeTab === i ? "active" : ""}
                        onClick={() => setActiveTab(i)}
                    >
                        {tab}
                    </button>
                ))}
            </div>

            <div className="sidebar-panel">
                {activeTab === 0 && <FiltersPanel />}
                {activeTab === 1 && <FeaturesPanel />}
                {activeTab === 2 && <VisualizationPanel />}
            </div>
        </div>
    );
}