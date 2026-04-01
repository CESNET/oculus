import { useState } from "react";
import FiltersTab from "./FiltersTab.tsx";
import FeaturesTab from "./FeaturesTab.tsx";
import VisualizationTab from "./VisualizationTab.tsx";
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
                {activeTab === 0 && (
                    <FiltersTab onFetched={() => setActiveTab(1)} />
                )}
                {activeTab === 1 && <FeaturesTab />}
                {activeTab === 2 && <VisualizationTab />}
            </div>
        </div>
    );
}