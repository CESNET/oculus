import React from 'react';
import ControlPanelContainer from './components/controlPanel/ControlPanelContainer';
import MapContainerWrapper from './components/map/MapContainerWrapper';
import './App.css'; // globální layout

const App: React.FC = () => {
    return (
        <div className="app-container">
            <ControlPanelContainer />
            <div className="map-container">
                <MapContainerWrapper />
            </div>
        </div>
    );
};

export default App;