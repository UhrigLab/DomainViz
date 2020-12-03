import React, { useState } from 'react';
//import request from 'utils/Request'; TODO refactor to remove burden from ProtPlot.js
import axios from 'axios';
import UploadFile from './UploadFile';
import AccordionSetup from './AccordionSetup';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { Button, Checkbox, FormControlLabel, TextField, Typography } from '@material-ui/core';
import { Alert, AlertTitle } from '@material-ui/lab';
import { Route, useHistory } from 'react-router';

//TODO: change color palette (Eg. 191D32, 7f7f7f, 423B0B, D000000, FFBA08[replace with mustard yellow?])
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

//generates random id;
let guid = () => {
    let s4 = () => {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    //return id of format 'aaaaaaaa'-'aaaa'-'aaaa'-'aaaa'-'aaaaaaaaaaaa'
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}

function ProtPlot() {
    //temp for production
    function getImages() {
        history.push('/view-results/' + textFields.uidTextField);
      }
    //end of temp
    const classes = useStyles();
    const resultID = guid();
    const history = useHistory()

    let fastaFile = null;
    let fileReader;

    const [checkboxes, setCheckboxes] = useState({
        absoluteResultsCheckbox: false,
    });
    const handleCheckBox = (event) => {
        setCheckboxes({ ...checkboxes, [event.target.name]: event.target.checked });
    };

    const [textFields, setTextFields] = useState({
        cutoffTextField: '0.05',
        maxCutoffTextField: '0.05',
        scaleFigureTextField: '1',
    });
    const handleTextField = (event) => {
        setTextFields({ ...textFields, [event.target.name]: event.target.value })
    }

    const handleFileRead = (e) => {
        const content = fileReader.result;
        //TODO Validate file content
        console.log(content)
    }
    function handleFastaFile(file) {
        //only accept fasta file
        let valid = true;
        if (((file.size / 1024) / 1024).toFixed(4) > 10) {
            alert("Your fasta file is greater than 10mb, which is the maximum allowed size.")
            valid = false;
        }
        fileReader = new FileReader();
        fileReader.onloadend = handleFileRead;
        fileReader.readAsText(file);

        if (valid) {
            fastaFile = file;
            alert("Sucessfully uploaded file: " + file.name)
        }
        else {
            alert("Your fasta file is not in a valid format, please try again with a different file.")
        }
    }

    async function sendPartOneFiles() {
        //Save file to server so the backend can access it 
        const data = new FormData();

        if (fastaFile == null) {
            alert("Please upload a file before clicking go.");
            return;
        }
        data.append(resultID, fastaFile, fastaFile.name);

        //Validate fastaFile:

        if (checkboxes.absoluteResultsCheckbox) {
            console.log(checkboxes.absoluteResultsCheckbox.toString())
            data.append('absoluteResults', checkboxes.absoluteResultsCheckbox);
        }
        else {
            data.append('absoluteResults', checkboxes.absoluteResultsCheckbox);
        }
        if (textFields.cutoffTextField !== '') {
            if (parseFloat(textFields.cutoffTextField) < 0 || parseFloat(textFields.cutoffTextField) > 1) {
                alert("Please enter a valid cutoff value, or remove it.");
                return;
            }
            else {
                console.log(textFields.cutoffTextField);
                data.append('cutoff', parseFloat(textFields.cutoffTextField));
            }
        }
        if (textFields.maxCutoffTextField !== '') {
            if (parseFloat(textFields.maxCutoffTextField) < 0 || parseFloat(textFields.maxCutoffTextField) > 1) {
                alert("Please enter a valid maximum cutoff value, or remove it.");
                return;
            }
            else {
                console.log(textFields.maxCutoffTextField)
                data.append('maxCutoff', parseFloat(textFields.maxCutoffTextField));
            }
        }
        if (textFields.scaleFigureTextField !== '') {
            if (parseFloat(textFields.scaleFigureTextField) < 0) {
                alert("Please enter a valid figure scale value.");
                return;
            }
            else {
                console.log(textFields.scaleFigureTextField)
                data.append('scaleFigure', parseFloat(textFields.scaleFigureTextField));
            }
        }
        alert("Your unique id is: " + resultID + "\n Please save this, as you won't be able to view or download your files without it.")

        await axios.post('/api/sendfiles', data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        }).then(response => {
            console.log("done")
            console.log(response);
            textFields.scaleFigureTextField = '';
            textFields.maxCutoffTextField = '';
            textFields.cutoffTextField = '';
            checkboxes.absoluteResultsCheckbox = false;
            history.push("/view-results/" + resultID);
        }).catch(error => {
            console.log(error);
        });
    }

    return (
        <div className='protplot'>
            <div>
                <Grid container spacing={3} alignItems='center'>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined' style={{ marginTop: "70px" }}>Use DomainVis by first uploading your fasta file, and then adding options if desired, and finally press the Go button!</Paper>
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='fastatxt' header='Fasta File' body='The file needs to contain fasta sequences in files named either .fa or .fasta.'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='fasta' handleFile={handleFastaFile} acceptedTypes='.fa,.fasta' />
                    </Grid>
                    <Grid item xs={4}>
                        <AccordionSetup id='cutofftxt' header='Enter a number between 0 and 1.' body='Only domains occuring in a ratio higher than the number are plotted (e.g. If the value is 0.5, the domain has to occur somewhere in the protein of at least 50% of sequences).'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='cutoff' name='cutoffTextField' value={textFields.cutoffTextField} type='number' label='Cutoff' inputProps={{ step: '0.1', max: 1, min: 0 }} onChange={handleTextField} />
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='max-cutofftxt' header='Enter a number between 0 and 1.' body='Only domains that have a maximum prevalence at a relative place in the protein group above this ratio are plotted (e.g. if value is 0.5, 50% of the sequences have to have this domain at the same relative position).'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='max-cutoff' name='maxCutoffTextField' value={textFields.maxCutoffTextField} type='number' label='Max Cutoff' inputProps={{ step: '0.1', max: 1, min: 0 }} onChange={handleTextField} />
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='scale-figuretxt' header='Enter a number larger than 0.' body='The number you input represents the number of inches per 100pb that the plot is used to display.'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='scale-figure' name='scaleFigureTextField' value={textFields.scaleFigureTextField} type='number' label='Scale Figure' inputProps={{min: 0}} onChange={handleTextField} />
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='absoluteresultstxt' header='Do you want absolute results?' body='Absolute results means that we will plot absolute numbers on y axis of plots instead of relative ones. If the box is unchecked, we plot relative results, if it is checked, we plot absolute results.'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <FormControlLabel
                            control={<Checkbox checked={checkboxes.absoluteResultsCheckbox} onChange={handleCheckBox} name="absoluteResultsCheckbox" />}
                            label="Yes/No" />
                    </Grid>

                    <Grid item xs={12}>
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={sendPartOneFiles}>
                            Go
                        </Button>
                    </Grid>
                     {/* temp for production */}
                    <Grid item xs={5}>
                        <Typography variant='body1'>Already have a code? Enter it here:</Typography>
                    </Grid>
                    <Grid item xs={1}>
                        <TextField id='uid' name='uidTextField' value={textFields.uidTextField} label='User ID' type="text" onChange={handleTextField} />
                    </Grid>
                    <Grid item xs={6}>
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={getImages}>Go to my Results!</Button>
                    </Grid>
                     {/* end of temp */}
                </Grid>
            </div>
        </div>
    );
}

export default ProtPlot;
