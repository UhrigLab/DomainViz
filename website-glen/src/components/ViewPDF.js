import React, { useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Grid, Paper } from '@material-ui/core';

export const ViewPDF = () => {
    const url = window.location.pathname;
    let uid =  url.split("/view-results/")[1]
    console.log(uid)
    const [images, setImages] = useState([]);
    useEffect(() => {
        fetch('/images/' + uid).then(response => 
            response.json().then(data => {
                setImages(data.images);
                console.log(images);
            })
        );
    }, []);
    return (
        <>
            <Grid container spacing={3}>
                {images.map(image => {
                    return (
                        <>
                            {/* <Grid item xs={6}>
                                <Paper variant='outlined'>{image.filepath.split(uid)[1]}</Paper>
                            </Grid>
                            <Grid item xs={6}>
                                <PDF pdf={process.env.PUBLIC_URL + image.filepath.split('public')[1]}></PDF>
                            </Grid> */}
                            <Grid item xs={6}>
                                {/* <Paper variant='outlined'>{image.filepath.split(uid)[1]}</Paper> */}
                            </Grid>
                            <Grid item xs={6}>
                                <PDF pdf={image.file}></PDF>
                            </Grid> 
                        </>
                    )
                })}
            </Grid>
       </>
    );
}