import React from 'react';
import { Tabs, Tab } from 'react-bootstrap';
import TimeFilter from './filters/TimeFilter';
import CoordinatesInput from './filters/CoordinatesInput';
import FeatureList from './features/FeatureList';
import VisualizationPanel from './visualization/VisualizationPanel';

const ControlPanelTabs: React.FC = () => {
    return (
        <Tabs defaultActiveKey="filters" className="p-2">
            <Tab eventKey="filters" title="Filters">
                <div className="p-2">
                    <TimeFilter />
                    <CoordinatesInput />
                </div>
            </Tab>

            <Tab eventKey="features" title="Features">
                <div className="p-2">
                    <FeatureList />
                </div>
            </Tab>

            <Tab eventKey="visualization" title="Visualization">
                <div className="p-2">
                    <VisualizationPanel />
                </div>
            </Tab>
        </Tabs>
    );
};

export default ControlPanelTabs;