import React, { useState } from 'react';
import { Page } from 'react-pdf';
import { Document } from 'react-pdf/dist/esm/entry.webpack';

export const PDF = ({pdf}) => {

    const [numPages, setNumPages] = useState(null);
    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
    }

    
    return (
        <Document
            file={ pdf }
            onLoadSuccess={onDocumentLoadSuccess}
        >

            {Array.from(new Array(numPages), (el, index) => (
                <Page key={`page_${index + 1}`} pageNumber={index + 1} />
            ))}

        </Document>
    );
} 