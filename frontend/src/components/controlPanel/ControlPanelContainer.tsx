import React, { useState } from 'react';
import ControlPanelTabs from './ControlPanelTabs';
import 'bootstrap/dist/css/bootstrap.min.css';
import './ControlPanelContainer.css';

const ControlPanelContainer: React.FC = () => {
    const [open, setOpen] = useState(false);

    const toggleOpen = () => setOpen(!open);

    return (
        <>
            {/* Desktop sidebar */}
            <div className="control-panel-desktop d-none d-md-flex flex-column">
                <ControlPanelTabs />
            </div>

            {/* Mobile overlay panel */}
            <div className={`mobile-overlay d-md-none ${open ? 'open' : ''}`}>
                <div className="mobile-overlay-content">
                    <ControlPanelTabs />
                </div>

                {/* Šipka dole uvnitř panelu */}
                <div className="mobile-toggle-btn" onClick={toggleOpen}>
                    <span className={`arrow ${open ? 'open' : ''}`}>˅</span>
                </div>
            </div>

            {/* Šipka nahoře uprostřed pokud panel zavřený */}
            {!open && (
                <div className="mobile-toggle-top d-md-none" onClick={toggleOpen}>
                    <span className="arrow">˅</span>
                </div>
            )}
        </>
    );
};

export default ControlPanelContainer;