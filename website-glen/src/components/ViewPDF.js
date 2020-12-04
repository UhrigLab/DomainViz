import { React, useEffect, useState } from 'react';
import { PDFMap } from './utils/PDFMap';
import { ProgressBar } from './utils/ProgressBar';
import { Typography, Grid, Paper, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
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
    const [open, setOpen] = useState(false);
    const classes = useStyles();

    let history = useHistory();
    let uid = url.split("/view-results/")[1];

    function goToHome() {
        history.push('/')
    }
    const handleClickOpen = () => {
        setOpen(true);
      };
    
      const handleClose = () => {
        setOpen(false);
      };

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
                            clearInterval(interval);
                        }
                        else if (data.failed < 5) {
                            setShowProgressBar(true);
                            setProgress(data.failed);
                        }
                    }
                })
            );
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <>
            <Grid container spacing={3}>
                <Grid style={{ marginTop: "70px" }} item xs={12}></Grid>

                <Grid item xs={12}>
                    <Paper className={classes.paper} variant='outlined'>
                        <Typography variant='h5'>{"Result id: " + uid}</Typography>
                    </Paper>
                </Grid>

                {(images.length > 0 && !showProgressBar && !failed) &&
                    <PDFMap images={images} uid={uid} />
                }
                {(images.length == 0 && showProgressBar && !failed) &&
                    <ProgressBar progress />
                }
                <Grid item xs={12}>
                    <Paper className={classes.paper} variant='outlined'>
                        {(images.length == 0 && !showProgressBar && failed) &&
                            <Typography variant='h5'>Something went wrong. Please try again.</Typography>
                        }
                        {(images.length == 0 && !showProgressBar && !failed) &&
                            <Typography variant='h5'>Loading, please wait...</Typography>
                        }
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Button variant='contained' color='primary' component='span' className={classes.button} onClick={handleClickOpen}>Done</Button>
                    <Dialog
                        open={open}
                        onClose={handleClose}
                        aria-labelledby="alert-dialog-title"
                        aria-describedby="alert-dialog-description"
                    >
                        <DialogTitle id="alert-dialog-title">{"Have you saved your result id?"}</DialogTitle>
                        <DialogContent>
                            <DialogContentText id="alert-dialog-description">
                                If you want to return to view your results again, you must save your result id. 
                                If you do not save your result id, YOU WILL NOT BE ABLE TO VIEW THIS PAGE AGAIN
                            </DialogContentText>
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={handleClose} color="primary">
                                No
                            </Button>
                            <Button onClick={goToHome} color="primary" autoFocus>
                                Yes
                            </Button>
                        </DialogActions>
                    </Dialog>
                </Grid>
            </Grid>
        </>
    );
}
