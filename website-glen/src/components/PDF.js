import React, { useMemo, useState } from 'react';
import { Page } from 'react-pdf';
import { Document } from 'react-pdf/dist/esm/entry.webpack';

export const PDF = ({pdf}) => {

    const [numPages, setNumPages] = useState(null);
    function onDocumentLoadSuccess({ numPages }) {
        console.log("Successfully displayed pdf")
        setNumPages(numPages);
    }

    let pdf_string = 'data:application/pdf;base64,' + pdf;

    return (
        <Document
            file={pdf_string}
            onLoadSuccess={onDocumentLoadSuccess}
            
        >

            {Array.from(new Array(numPages), (el, index) => (
                <Page key={`page_${index + 1}`} pageNumber={index + 1} />
            ))}

        </Document>
    );
} 