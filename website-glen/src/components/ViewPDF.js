import React, { useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Paper, CircularProgress, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import {saveAs} from 'file-saver';
import { useHistory } from 'react-router-dom';


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

    let history = useHistory();
    let uid = url.split("/view-results/")[1];

    function gotoDownload() {
        fetch('/api/download/' + uid).then(response => {
            saveAs(response.url, uid + '.zip')
          });
        
    }
    function goToHome() {
        history.push('/')
    }

    useEffect(() => {
        const interval = setInterval(() => {
            fetch('/api/images/' + uid).then(response =>
                response.json().then(data => {
                    console.log(data);
                    if (data.hasOwnProperty('images')) {
                        setImages(data.images);
                        clearInterval(interval);
                    }
                    else {
                        if (data.failed === 'null') {
                            alert("Oh dear, we don't seem to have any information under that ID. Please try again.");
                            setFailed(true);
                            clearInterval(interval);
                        }
                        else if (data.failed === -1) {
                            alert("Oh dear, this attempt failed. Please double-check your data and try running ProDoPlot again.");
                            setFailed(true);
                        }
                        else if (data.failed < 5) {
                            setShowProgressBar(true);
                            setProgress(data.failed);
                            clearInterval(interval);
                        }
                    }
                })
            );
        }, 5000);
        return () => clearInterval(interval);
    }, []);


    if (images.length > 0) {
        return (
            <>
                <Grid container spacing={3}>
                    <Grid style={{marginTop: "70px"}} item xs={12}></Grid>
                    <Grid item xs={12}></Grid>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined'>
                            <Typography variant='h5'>{"Result id: " + uid}</Typography>
                        </Paper>
                    </Grid>
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
                    <Grid item xs={12}>
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={gotoDownload}>Download</Button>
                    </Grid>
                    <Grid item xs={12}>
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={goToHome}>Done</Button>
                    </Grid>

                </Grid>
            </>
        );
    }
    else if (showProgressBar) {
        return (
            <>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined'>
                            <Typography variant='h5'>{"Result id: " + uid}</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined' style={{marginTop: "70px"}}>                
                            <Typography variant='h5'>Loading, this may take a while, please wait...</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <CircularProgress variant='static' value={progress*20} style={{marginTop: "70px"}}></CircularProgress>
                    </Grid>
                    <Grid item xs={12}>
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={goToHome}>Done</Button>
                    </Grid>
                </Grid>
            </>
        );
    }
    else if (failed) {
        return (
            <>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined'>
                            <Typography variant='h5'>{"Result id: " + uid}</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined' style={{marginTop: "70px"}}>                
                            <Typography variant='h5'>Something went wrong. Please try again.</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={goToHome}>Done</Button>
                    </Grid>
                </Grid>
            </>
        );
    }
    else {
        return (
            <>
                <Grid container spacing={3}>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined'>
                            <Typography variant='h5'>{"Result id: " + uid}</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined' style={{marginTop: "70px"}}>                
                            <Typography variant='h5'>Loading, please wait...</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={goToHome}>Done</Button>
                    </Grid>
                </Grid>
            </>
        );
    }
}
