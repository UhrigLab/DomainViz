import React, { useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Grid, Paper } from '@material-ui/core';
//39341b3e-908e-f89a-3715-99087486dbfc
const pdfContext = require.context('./tmp', false, /\.pdf$/);
const pdfFiles = pdfContext
.keys()
.map((filename) => pdfContext(filename))
console.log(pdfContext.keys())
console.log(pdfFiles)

export const ViewPDF = () => {
    const url = window.location.pathname;
    let uid =  url.split("/view-results/")[1]
    const [images, setImages] = useState([]);
    useEffect(() => {
        fetch('/images/' + uid).then(response => 
            response.json().then(data => {
                setImages(data.images)
            })
        );
    }, []);
 
    return (
        <>
            <Grid container spacing={3}>
                {/* {images.map(image => {
                    return (
                        <>
                            <Grid item xs={6}>
                                <Paper variant='outlined'>{image.filepath.split(uid)[1]}</Paper>
                            </Grid>
                            <Grid item xs={6}>
                                <PDF pdf={image.filepath}></PDF>
                            </Grid>
                        </>
                    )
                })} */}
                {pdfFiles.map((pdf, index) => {
                    return (
                        <>
                            <Grid item xs={6}>
                                <Paper variant='outlined'>Blah</Paper>
                            </Grid>
                            <Grid item xs={6}>
                                <PDF pdf={"./39341b3e-908e-f89a-3715-99087486dbfc_ProteinGroup_combined.pdf"}></PDF>
                            </Grid>
                        </>
                    )
                })}
            </Grid>
       </>
    );
}