import React, { useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Paper, CircularProgress } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    button: {
        padding: theme.spacing(1),
        textAlign: 'center',
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
  }));
export const ViewPDF = () => {
    const url = window.location.pathname;
    const [images, setImages] = useState([]);
    const [progress, setProgress] = useState(0);
    const [showProgressBar, setShowProgressBar] = useState(false)
    const [failed, setFailed] = useState(false);
    const groupsize = 3;
    const classes = useStyles();

    let uid = url.split("/view-results/")[1];
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
                            if (data.failed === 'null') {
                                alert("Oh dear, we don't seem to have any information under that ID. Please try again.");
                                setFailed(true);
                            }
                            else if (data.failed === -1) {
                                alert("Oh dear, this attempt failed. Please double-check your data and try running ProDoPlot again.");
                                setFailed(true);
                            }
                            else if (data.failed < 5) {
                                alert("Your data is in progress, please wait.");
                                setShowProgressBar(true);
                                setProgress(data.failed);
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
                    <Grid style={{marginTop: "70px"}} item xs={12}></Grid>
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
            <>
                <Paper className={classes.paper} variant='outlined' style={{marginTop: "70px"}}>                
                    <Typography variant='h5'>Loading, this may take a while, please wait...</Typography>
                </Paper>
                <CircularProgress variant='static' value={progress*20} style={{marginTop: "70px"}}></CircularProgress>
            </>
        );
    }
    else {
        return (
            <>
                <Paper className={classes.paper} variant='outlined' style={{marginTop: "70px"}}>                
                    <Typography variant='h5'>Loading, please wait...</Typography>
                </Paper>
            </>
        );
    }
}
