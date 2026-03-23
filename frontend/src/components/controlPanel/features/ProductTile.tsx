import React from 'react';
import {Card} from 'react-bootstrap';

interface Props {
    name: string;
}

const ProductTile: React.FC<Props> = ({name}) => {
    return (
        <Card className="mb-2">
            <Card.Body>{name}</Card.Body>
        </Card>
    );
};

export default ProductTile;