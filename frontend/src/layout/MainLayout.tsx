import {Container, Row, Col} from "react-bootstrap";

import {useRef} from "react";

import NavbarLayout from "./NavbarLayout";
import SidebarLayout from "./SidebarLayout";
import MapLayout from "./MapLayout.tsx";

import './MainLayout.css';

export default function MainLayout() {
    // Sdílený ref pro programmatic posuny mapy
    const programmaticRef = useRef(false);

    return (
        <div className="main-layout">
            <NavbarLayout programmaticRef={programmaticRef} />

            <Container fluid className="main-container">
                <Row>
                    <Col md={3} className="p-0 sidebar-col">
                        <SidebarLayout />
                    </Col>

                    <Col md={9} className="p-0 map-col">
                        <MapLayout programmaticRef={programmaticRef} />
                    </Col>
                </Row>
            </Container>
        </div>
    );
}