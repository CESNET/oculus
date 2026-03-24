import { Container, Row, Col } from "react-bootstrap";

import NavbarLayout from "./NavbarLayout";
import SidebarLayout from "./SidebarLayout";
import MapLayout from "./MapLayout.tsx";

import './MainLayout.css';

export default function MainLayout() {
    return (
        <div className="main-layout">
            <NavbarLayout />

            <Container fluid className="main-container">
                <Row className="h-100">
                    <Col md={3} className="p-0 sidebar-col">
                        <SidebarLayout />
                    </Col>

                    <Col md={9} className="p-0 map-col">
                        <MapLayout />
                    </Col>
                </Row>
            </Container>
        </div>
    );
}