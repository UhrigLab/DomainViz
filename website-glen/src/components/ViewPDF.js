import React, { useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Grid, Paper } from '@material-ui/core';

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
                {images.map((image, index) => {
                    return (
                        <>
                            <Grid item xs={2}>
                                <Paper variant='outlined'>{"Group "+(index/groupsize)}</Paper>
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
