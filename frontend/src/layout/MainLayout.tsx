import { useRef, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";

import LoadingOverlay from "../components/ui/LoadingOverlay";
import NavbarLayout from "./NavbarLayout";
import SidebarLayout from "./SidebarLayout";
import MapLayout from "./MapLayout";
import "./MainLayout.css";

export default function MainLayout() {
    const programmaticRef = useRef(false);
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);

    return (
        <div className="main-layout">
            <LoadingOverlay />

            <NavbarLayout programmaticRef={programmaticRef} />

            <Container
                fluid
                className={`main-container ${
                    isSidebarOpen ? "sidebar-is-open" : "sidebar-is-closed"
                }`}
            >
                <Row>
                    <Col
                        className={`p-0 sidebar-col ${
                            isSidebarOpen
                                ? "sidebar-col--open"
                                : "sidebar-col--closed"
                        }`}
                    >
                        <div className="sidebar-panel-content">
                            <SidebarLayout />
                        </div>

                        <button
                            type="button"
                            className="sidebar-toggle-button sidebar-close-button"
                            onClick={() => setIsSidebarOpen(false)}
                            aria-label="Collapse sidebar"
                            aria-expanded={isSidebarOpen}
                            title="Collapse sidebar"
                            tabIndex={isSidebarOpen ? 0 : -1}
                        >
                            <i
                                className="bi bi-chevron-left sidebar-icon-desktop"
                                aria-hidden="true"
                            />
                            <i
                                className="bi bi-chevron-up sidebar-icon-mobile"
                                aria-hidden="true"
                            />
                        </button>
                    </Col>

                    <button
                        type="button"
                        className="sidebar-toggle-button sidebar-open-button"
                        onClick={() => setIsSidebarOpen(true)}
                        aria-label="Open sidebar"
                        aria-expanded={isSidebarOpen}
                        title="Open sidebar"
                        tabIndex={isSidebarOpen ? -1 : 0}
                    >
                        <i
                            className="bi bi-chevron-right sidebar-icon-desktop"
                            aria-hidden="true"
                        />
                        <i
                            className="bi bi-chevron-down sidebar-icon-mobile"
                            aria-hidden="true"
                        />
                    </button>

                    <Col className="p-0 map-col">
                        <MapLayout programmaticRef={programmaticRef} />
                    </Col>
                </Row>
            </Container>
        </div>
    );
}