import React, {useState} from 'react';
import {Form, Row, Col} from 'react-bootstrap';

const CoordinatesInput: React.FC = () => {
    const [lat, setLat] = useState('');
    const [lng, setLng] = useState('');

    return (
        <Form className="mt-2">
            <Row>
                <Col>
                    <Form.Group>
                        <Form.Label>Latitude</Form.Label>
                        <Form.Control
                            type="number"
                            value={lat}
                            onChange={(e) => setLat(e.target.value)}
                        />
                    </Form.Group>
                </Col>
                <Col>
                    <Form.Group>
                        <Form.Label>Longitude</Form.Label>
                        <Form.Control
                            type="number"
                            value={lng}
                            onChange={(e) => setLng(e.target.value)}
                        />
                    </Form.Group>
                </Col>
            </Row>
        </Form>
    );
};

export default CoordinatesInput;