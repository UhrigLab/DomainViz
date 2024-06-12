import { React, useState, Fragment } from 'react';
import { Button, Grid, makeStyles, TextField, Typography, Paper } from '@material-ui/core';


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
        color: theme.palette.text.primary,
    },
}));


export const FastaFileMap = ({ fastaFiles, changeName, removeFile }) => {
    /* This component displays the fasta files after they are uploaded, and gives the user the option to
     * perform actions such as deletion, and renaming of each file.
     * 
     * As a `Map` component, this component receives a list of objects, fasta files in this instance,
     * and displays each object in a way that allows reusability, and conciseness. However, this component may be improved
     * by making it more customizable, and more general, ie, making it more of a FileMap.
     * 
     * Must be used inside of a Grid container component.
     */

    const classes = useStyles();
    const [faFileNames, setFAFileNames] = useState([]);

    const handleFAFilesChange = (event, faFileName, index) => {
        if (faFileNames.length < fastaFiles.length) {
            let names = []
            for (let i=0; i<fastaFiles.length; i++) {
                names.push(fastaFiles[i].name);
            }
            setFAFileNames([
                ...names.slice(0, index),
                faFileName,
                ...names.slice(index+1)
            ]);
        }
        else {
            setFAFileNames([
                ...faFileNames.slice(0, index),
                faFileName,
                ...faFileNames.slice(index+1)
            ]);
        }
    }

    const returnName = (event, index) => {
        if (faFileNames.length !== 0) {
            changeName(index, faFileNames[index]);
        }
        else {
            alert("Please change a name before clicking the \"Confirm\" button.")
        }
    }
    const deleteFile = (event, index) => {
        removeFile(index)
    }

    return (
        <>
            {/* Each file will have the following. */}
            {fastaFiles.map((file, i) => {
                return (
                    // Since this component must exist inside of a Grid container component, we don't add a second container.
                    <Fragment key={i}>
                        <Grid item xs={2}/>
                        <Grid item xs={3}>
                            <Paper className={classes.paper} variant='outlined'>
                                <Typography>{file.name}</Typography>
                            </Paper>
                        </Grid>
                        <Grid item xs={2}>
                            <TextField fullWidth name={`fasta-filename-${i}`} label='New Name' onChange={(e) => handleFAFilesChange(e, e.target.value, i)}/>
                        </Grid>
                        <Grid item xs={1}>
                            <Button name={`rename-button-${i}`} variant='contained' color='default' component='span' className={classes.button} onClick={(e) => returnName(e, i)}>Confirm</Button>
                        </Grid>
                        <Grid item xs={1}>
                            <Button name={`delete-button-${i}`} variant='contained' color='default' component='span' className={classes.button} onClick={(e) => deleteFile(e, i)}>Clear Entry</Button>
                        </Grid>
                        <Grid item xs={3}/>
                    </Fragment>
                )
            })}
        </>
    );
}