import React, { useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Paper } from '@material-ui/core';

export const ViewPDF = () => {
    const url = window.location.pathname;
    let uid =  url.split("/view-results/")[1]
    console.log(uid)
    const [images, setImages] = useState([]);
    const groupsize = 3;
    useEffect(() => {
        fetch('/api/images/' + uid).then(response => 
            response.json().then(data => {
                setImages(data.images);
                console.log(images);
            })
        );
    }, []);
    return (
        <>
            <Grid container spacing={3}>
            <Grid item xs={12}></Grid>
            <Grid item xs={12}></Grid>
            <Grid item xs={12}></Grid>


                {images.map((image, index) => {
                    return (
                        <>
                            <Grid item xs={2}>
                                <Typography variant='h5'>{"Group "+(index/groupsize)}</Typography>
                            </Grid>
                            <Grid item xs={2}>
                                <PDF pdf={image.file}></PDF>
                            </Grid> 
                        </>
                    )
                })}
            </Grid>
       </>
    );
}
