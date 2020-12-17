import { Typography } from '@material-ui/core';
import React, { useState } from 'react';
import { Page } from 'react-pdf';
import { Document } from 'react-pdf/dist/esm/entry.webpack';

export const PDF = ({pdf}) => {

    const [numPages, setNumPages] = useState(null);
    const [didError, setDidError] = useState(false);

    function onDocumentLoadSuccess({ numPages }) {
        console.log("Successfully displayed pdf");
        setNumPages(numPages);
    }
    function onDocumentLoadError() {
        alert("Results not loaded. The page will reload and try again.");
        setDidError(true);
        window.location.reload();
    }

    let pdf_string = 'data:application/pdf;base64,' + pdf;

    return (
        <>
            <Document
                file={pdf_string}
                onLoadSuccess={onDocumentLoadSuccess}
                onLoadError={onDocumentLoadError}
            >

                {Array.from(new Array(numPages), (el, index) => (
                    <Page key={`page_${index + 1}`} pageNumber={index + 1} />
                ))}

            </Document>
            {(didError) &&
                <Typography variant='h6'>Oh dear. Something went wrong loading this pdf. Please reload the website.</Typography>
            }
        </>
    );
} 