import { React, useEffect, useState } from 'react';
import { PDFMap } from './utils/PDFMap';
import { MessageMap } from './utils/MessageMap';
import { Typography, Grid, Paper, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, CircularProgress, TextField } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { useHistory } from 'react-router-dom';
import DomainVizIcon from './img/domainviz.png';
import { saveAs } from 'file-saver';
import { ColorGroupMap } from './utils/ColorGroupMap';


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
    img: {
        height: "122px",
        width: "293px"
    },
}));
let interval;

export const ViewPDF = () => {
    const url = window.location.pathname;
    const [images, setImages] = useState([]);
    const [groupNames, setGroupNames] = useState([]);
    const [displayImages, setDisplayImages] = useState(false);
    const [currentMessage, setCurrentMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [progress, setProgress] = useState(0);
    const [showProgressBar, setShowProgressBar] = useState(false);
    const [showColorDialog, setShowColorDialog] = useState(false);
    const [colorGroups, setColorGroups] = useState([])
    const [failed, setFailed] = useState(false);
    const [showExitDialog, setShowExitDialog] = useState(false);
    const classes = useStyles();
    const [open, setOpen] = useState(false);

    const classes = useStyles();
    let history = useHistory();

    let uid = url.split("/view-results/")[1];

    function goToHome() {
        history.push('/')
    }
    const handleClickOpenExitDialog = () => {
        setShowExitDialog(true);
    };
    const handleCloseExitDialog = () => {
        setShowExitDialog(false);
    };

    function gotoChangeColors() {
        //Clear the colors
        setColorGroups([])
        fetch('/api/color-files/' + uid).then(response =>
            response.json().then(data => {
                //get the JSONified color group data from the backend, and put it into the colorGroups state
                for (let i in data.colorGroups) { 
                    let group = data.colorGroups[i].split('\t')[0];
                    let hexcode = data.colorGroups[i].split('\t')[1];
                    let colorDict = {"group": group, "color": hexcode}
                    setColorGroups(current => [...current, colorDict])
                }
                setShowColorDialog(true);
            })
        );
    }
    const handleCloseColorDialog = () => {
        setShowColorDialog(false);
    };

    function gotoDownload() {
        fetch('/api/download/' + uid).then(response => {
            saveAs(response.url, 'DomainViz_results.zip')
        });
    }

    useEffect(() => {
        interval = setInterval(() => {
            fetch('/api/images/' + uid).then(response =>
                response.json().then(data => {
                    if (data.hasOwnProperty('images')) {
                        setImages(data.images);
                        setGroupNames(data.groups)
                    }
                    else {
                        if (data.failed === 'null') {
                            alert("Oh dear, we don't seem to have any information under that ID. Please try again.");
                            setFailed(true);
                        }
                        else if (data.failed === 'notready') {
                            //TODO remove temp
                            //TEMP:
                            alert("Results not loaded, please refresh the page.")
                            setFailed("TEMP");
                            //END OF TEMP
                        }
                        else if (data.failed === -1) {
                            alert("Oh dear, this attempt failed. Please double-check your data and try running DomainViz again.");
                            setFailed(true);
                            try {
                                if (data.info.length > 0) {
                                    setCurrentMessage(data.info);
                                }
                            } catch {
                                console.log("No message was found with this cookie: Cookie -1.")
                            }
                        }
                        else if (data.failed < 100) {
                            setShowProgressBar(true);
                            setProgress(data.failed);
                            try {
                                if (data.info.length > 0) {
                                    setCurrentMessage(data.info);
                                }
                            } catch {
                                console.log("No message was found with this cookie: Cookie " + data.failed + ".")
                            }
                        }
                    }
                })
            );
        }, 5000);
        return () => clearInterval(interval);
    }, []);
    useEffect(() => {
        if (images.length > 0) {
            setDisplayImages(true);
            setShowProgressBar(false);
            clearInterval(interval);
        }
        if (failed) {
            clearInterval(interval);
        }
        if (!messages.includes(currentMessage) && currentMessage.length > 0) {
            setMessages(currentMessages => [...currentMessages, currentMessage]);
        }
    }, [images, failed, currentMessage]);

    return (
        <Grid container spacing={3} alignItems='center' style={{marginTop: '90px'}}>
            <Grid item xs={12}>
                <img src={DomainVizIcon} className={classes.img}></img>
            </Grid>

            <Grid item xs={12}>
                <Paper className={classes.paper} variant='outlined'>
                    <Typography variant='h5'>{"Result id: " + uid}</Typography>
                </Paper>
            </Grid>

            {(displayImages && !showProgressBar && failed == false) &&
                <>
                    <PDFMap images={images} uid={uid} groupNames={groupNames} />
                    <Grid item xs={12}>
                        <Button variant='contained' color='default' component='span' className={classes.button} onClick={gotoDownload}>Download</Button>
                        <Button variant='contained' color='default' component='span' className={classes.button} style={{ marginLeft: "10px" }} onClick={gotoChangeColors}>Change Colors</Button>
                    </Grid>
                    <Grid item xs={12}/>
                </>
            }
            {(!displayImages && showProgressBar && failed == false) &&
                <>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined'>
                            {(messages.length) && //If the message only contains whitespace, display the loading text
                                <MessageMap messages={messages}></MessageMap>
                            }
                            <Typography variant='h5'>Task processing can take several minutes to several hours. Please wait or copy the Result ID, exit, and retrieve your results later using the homepage.</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <CircularProgress variant='static' value={progress} color='secondary'></CircularProgress>
                    </Grid>
                </>
            }
            {/* TODO remove TEMP */}
            {(!displayImages && !showProgressBar && failed === "TEMP") &&
                <Grid item xs={12}>
                    <Paper className={classes.paper} variant='outlined'>
                        {/* <Typography variant='h5'>Something went wrong. Please try again.</Typography> */}
                        <Typography variant='h5'>Please try reloading the page.</Typography>

                        {(messages.length) //If the message has information, display the message
                            ? <MessageMap messages={messages}></MessageMap>
                            : <Typography variant='h5'>There was no information from this run.</Typography>
                        }
                    </Paper>
                </Grid>
            }
            {(!displayImages && !showProgressBar && failed) &&
                <Grid item xs={12}>
                    <Paper className={classes.paper} variant='outlined'>
                        <Typography variant='h5'>There is no information under that result id. Please choose a valid result id and try again.</Typography>
                    </Paper>
                </Grid>
            }
            {(!displayImages && !showProgressBar && !failed) &&
                <Grid item xs={12}>
                    <Paper className={classes.paper} variant='outlined'>
                        <Typography variant='h5'>Loading, please wait...</Typography>
                    </Paper>
                </Grid>
            }
            {(showColorDialog) &&
                <Dialog open={showColorDialog} onClose={handleCloseColorDialog} aria-labelledby="color-form-dialog-title">
                    <DialogTitle id="color-form-dialog-title">Change Group Coloring</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                            TEMPORORY TEXT
                        </DialogContentText>
                        <ColorGroupMap colorGroups={colorGroups}/>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCloseColorDialog}>Cancel</Button>
                        <Button onClick={handleCloseColorDialog}>Save</Button>
                    </DialogActions>
                </Dialog>
            }

            <Grid item xs={12}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={handleClickOpenExitDialog}>Exit</Button>
                <Dialog open={showExitDialog} onClose={handleCloseExitDialog} aria-labelledby="exit-dialog-title" aria-describedby="exit-dialog-description">
                    <DialogTitle id="exit-dialog-title">Have you saved your result id?</DialogTitle>
                    <DialogContent>
                        <DialogContentText id="alert-dialog-description">
                            If you want to return to view your results again, you must save your result id.
                            If you do not save your result id, YOU WILL NOT BE ABLE TO VIEW THIS PAGE AGAIN
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCloseExitDialog}>No</Button>
                        <Button onClick={goToHome} autoFocus>Yes</Button>
                    </DialogActions>
                </Dialog>
            </Grid>
        </Grid>
    );
}
