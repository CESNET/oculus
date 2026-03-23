import React from 'react';
import ProductTile from './ProductTile';
import {ListGroup} from 'react-bootstrap';

const FeatureList: React.FC = () => {
    // TODO: později fetch z Copernicus / backend
    const dummyFeatures = [
        {id: '1', name: 'Feature 1'},
        {id: '2', name: 'Feature 2'},
    ];

    return (
        <ListGroup className="mt-2">
            {dummyFeatures.map((f) => (
                <ListGroup.Item key={f.id}>
                    <ProductTile name={f.name}/>
                </ListGroup.Item>
            ))}
        </ListGroup>
    );
};

export default FeatureList;