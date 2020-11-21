import React, { useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Paper, CircularProgress } from '@material-ui/core';

export const ViewPDF = () => {
    const url = window.location.pathname;
    const [images, setImages] = useState([]);
    const groupsize = 3;

    let uid = url.split("/view-results/")[1];
    let showProgressBar = false;
    let progress = 0;
    let failed = false;
    useEffect(() => {
        const interval = setInterval(() => {
            if (images.length == 0 && !failed) {
                fetch('/api/images/' + uid).then(response =>
                    response.json().then(data => {
                        console.log(data);
                        if (data.hasOwnProperty('images')) {
                            setImages(data.images);
                            console.log(images);
                            return () => clearInterval(interval);
                        }
                        else {
                            if (data.failed == 'null') {
                                alert("Oh dear, we don't seem to have any information under that ID. Please try again.");
                                failed=true;
                            }
                            else if (data.failed == -1) {
                                alert("Oh dear, this attempt failed. Please double-check your data and try running ProDoPlot again.");
                                failed=true;
                            }
                            else if (data.failed < 5) {
                                alert("Your data is in progress, you may watch the progress bar below");
                                showProgressBar = true;
                                progress = data.failed;
                            }
                        }
                    })
                );
            }
        }, 5000);
        return () => clearInterval(interval);
    }, []);
    if (images.length > 0) {
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
                                    <Typography variant='h5'>{"Group " + (index / groupsize)}</Typography>
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
    else if (showProgressBar) {
        return (
            //TODO implement progress bar
            <>
                <h3>A</h3>
                <CircularProgress variant='static' value={progress}></CircularProgress>
            </>
        );
    }
    else {
        return (
            <>
                <h3>A</h3>
                <Paper variant='outlined'>                
                    <Typography variant='h5'>Please return to the home page and try again.</Typography>
                </Paper>
            </>
        );
    }
}
