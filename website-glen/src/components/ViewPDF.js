import { React, useEffect, useState } from 'react';
import { PDFMap } from './utils/PDFMap';
import { MessageMap } from './utils/MessageMap';
import { 
    Typography, 
    Grid, 
    Paper, 
    Button, 
    Dialog, 
    DialogActions, 
    DialogContent, 
    DialogContentText, 
    DialogTitle, 
    CircularProgress 
} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { useHistory } from 'react-router-dom';
import DomainVizIcon from './img/domainviz.png';


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
export const groupsize = 6;


export const ViewPDF = () => {
    /* This functional component is a page for the user to view the outputs of their DomainViz run.
     * It could be extended to include outputs from UMotif as well, but this has not been done yet.
     * 
     * The name of the component is out-of-date, since now we use iframes rather than PDFs for the outputs on the site itself.
     *
     * Overall this component is too complex, and some of the work done here should be shunted off to other components.
     */
    const url = window.location.pathname;
    // TODO To many useState()s, needs refactoring
    const [images, setImages] = useState([]);
    const [groupNames, setGroupNames] = useState([]);
    const [displayImages, setDisplayImages] = useState(false);
    const [currentMessage, setCurrentMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [progress, setProgress] = useState(0);
    const [showProgressBar, setShowProgressBar] = useState(false);
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

    // This useEffect is very complex, but essentially it gets the output images from the backend, groups them based on their group names
    // displays the images if they exist, and if not, it shows both an alert, and a "failed" message on the page (Why did I do both?).
    // As well, it controls the progress wheel based on the cookie-completion value sent from the backend.
    //
    // It runs a GET request to the backend every 5 seconds for an update on the run's progress. Once the run has completed, 
    // it stops GET-ing from the backend.
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
                            //alert("Oh dear, we don't seem to have any information under that ID. Please try again.");
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
                        // If data.failed isn't -1, the run hasn't actually failed, but it is still in progress, with the failed
                        // number representing how far along in the run we are, from 1-100.
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
    }, [uid]);

    // This second useEffect() is run whenever the first useEffect() updates one of the important state variables, as can be seen in the
    // [images, failed, currentMessage, messages, groupNames.length] list.
    // This is what actually updates the UI with the message, or the iframes.
    useEffect(() => {
        if (images.length / groupNames.length === groupsize) {
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
    }, [images, failed, currentMessage, messages, groupNames.length]);

    return (
        <Grid container spacing={3} alignItems='center' style={{marginTop: '90px'}}>

            <Grid item xs={12}>
                <img src={DomainVizIcon} alt="DomainViz logo" className={classes.img}></img>
            </Grid>

            <Grid item xs={12}>
                <Paper className={classes.paper} variant='outlined'>
                    <Typography variant='h5'>{"Result id: " + uid}</Typography>
                </Paper>
            </Grid>

            {(displayImages && !showProgressBar && failed === false) &&
                // The <PDFMap> component is what actually displays the iframes.
                <PDFMap images={images} uid={uid} groupNames={groupNames} />
            }
            {(!displayImages && showProgressBar && failed === false) &&
                <>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined'>
                            {(messages.length) && //If the message only contains whitespace, display the loading text
                                // The <MessageMap> component shows a list of the messages that have been returned from the cookies
                                // produced in the backend.
                                <MessageMap messages={messages}></MessageMap>
                            }
                            <Typography variant='h5'>Task processing can take several minutes to several hours. Please wait or copy the Result ID, exit, and retrieve your results later using the homepage.</Typography>
                        </Paper>
                    </Grid>
                    <Grid item xs={12}>
                        <CircularProgress variant='determinate' value={progress} color='secondary'></CircularProgress>
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
            {/* End of TEMP */}
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
            {/* 
                This Grid item contains the Exit button, and the dialog popup that appears when the user tries to exit the page.
                While useful, we need to open this dialog when the user tries to navigate away from this page using other methods,
                such as the AppBar, or the browser navigation buttons.
            */}
            <Grid item xs={12}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={handleClickOpen} style={{marginBottom:"10px"}}>Exit</Button>
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
                        <Button onClick={handleClose}>
                            No
                            </Button>
                        <Button onClick={goToHome} autoFocus>
                            Yes
                            </Button>
                    </DialogActions>
                </Dialog>
            </Grid>

        </Grid>
    );
}
