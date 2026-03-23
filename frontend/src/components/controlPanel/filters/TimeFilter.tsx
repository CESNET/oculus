import React, {useState} from 'react';
import {Form} from 'react-bootstrap';

const TimeFilter: React.FC = () => {
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');

    return (
        <Form>
            <Form.Group className="mb-2">
                <Form.Label>Start Date</Form.Label>
                <Form.Control
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                />
            </Form.Group>
            <Form.Group>
                <Form.Label>End Date</Form.Label>
                <Form.Control
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                />
            </Form.Group>
        </Form>
    );
};

export default TimeFilter;