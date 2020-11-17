import React, { useState } from 'react';
//import request from 'utils/Request'; TODO refactor to remove burden from ProtPlot.js
import axios from 'axios';
import UploadFile from './UploadFile';
import AccordionSetup from './AccordionSetup';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { Button, Checkbox, FormControlLabel, TextField } from '@material-ui/core';
import {Alert, AlertTitle} from '@material-ui/lab';
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
    const classes = useStyles();
    const resultID = guid();
    const history = useHistory()

    let fastaFile = null;
    let proteinGroupsFile = null;
    let colorFile = null;
    let ignoreDomainsFile = null;

    const [checkboxes, setCheckboxes] = useState({
        absoluteResultsCheckbox: false,
    });
    const handleCheckBox = (event) => {
        setCheckboxes({ ...checkboxes, [event.target.name]: event.target.checked });
    };

    const [textFields, setTextFields] = useState({
        cutoffTextField: '',
        maxCutoffTextField: '',
        scaleFigureTextField: '',
    });
    const handleTextField = (event) => {
        setTextFields({ ...textFields, [event.target.name]: event.target.value })
    }

    function handleFastaFile(file) {
        //TODO Validate files
        //only accept fasta file

        fastaFile = file;
    }

    function handleProteinGroupsFile(file) {
        //TODO Validate files

        proteinGroupsFile = file;
    }
    function handleColorFile(file) {
        //TODO Validate files

        colorFile = file;
    }
    function handleIgnoreDomainsFile(file) {
        //TODO Validate files

        ignoreDomainsFile = file;
    }


    async function sendPartOneFiles() {
        //Save file to server so the backend can access it 
        const data = new FormData();

        if (fastaFile == null) {
            alert("Please upload a file before clicking go.");
            return;
        }
        //Validate fastaFile:


        // if (proteinGroupsFile !== null) {
        //     data.append(resultID, proteinGroupsFile, proteinGroupsFile.name);
        // }
        // if (colorFile !== null) {
        //     data.append(resultID, colorFile, colorFile.name);
        // }
        // if (ignoreDomainsFile !== null) {
        //     data.append(resultID, ignoreDomainsFile, ignoreDomainsFile.name);
        // }

        // if (checkboxes.absoluteResultsCheckbox) {
        //     console.log(checkboxes.absoluteResultsCheckbox.toString())
        //     data.append(checkboxes.absoluteResultsCheckbox.name, checkboxes.absoluteResultsCheckbox);
        // }
        // else {
        //     data.append(checkboxes.absoluteResultsCheckbox.name, checkboxes.absoluteResultsCheckbox);
        // }
        // if (textFields.cutoffTextField !== '') {
        //     if (parseFloat(textFields.cutoffTextField) < 0 || parseFloat(textFields.cutoffTextField) > 1) {
        //         alert("Please enter a valid cutoff value, or remove it.");
        //         return;
        //     }
        //     else {
        //         console.log(textFields.cutoffTextField);
        //         data.append(textFields.cutoffTextField.name, parseFloat(textFields.cutoffTextField));
        //     }
        // }
        // if (textFields.maxCutoffTextField !== '') {
        //     if (parseFloat(textFields.maxCutoffTextField) < 0 || parseFloat(textFields.maxCutoffTextField) > 1) {
        //         alert("Please enter a valid maximum cutoff value, or remove it.");
        //         return;
        //     }
        //     else {
        //         console.log(textFields.maxCutoffTextField)
        //         data.append(textFields.maxCutoffTextField.name, parseFloat(textFields.maxCutoffTextField));
        //     }
        // }
        // if (textFields.scaleFigureTextField !== '') {
        //     if (parseFloat(textFields.scaleFigureTextField) < 0) {
        //         alert("Please enter a valid figure scale value.");
        //         return;
        //     }
        //     else {
        //         console.log(textFields.scaleFigureTextField)
        //         data.append(textFields.scaleFigureTextField.name, parseFloat(textFields.scaleFigureTextField));
        //     }
        // }
        alert("Your unique id is: " + resultID + "\n Please save this, as you won't be able to view or download your files without it.")
        data.append(resultID, fastaFile, fastaFile.name);
        await axios.post('/api/sendfiles', data, {
            headers: {
                //'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
                'Content-Type': 'multipart/form-data',
            }
        }).then(response => {
            console.log("done")
            console.log(response);
            alert("Success!");
            history.push("/view-results/" + resultID);
            // proteinGroupsFile = null;
            // colorFile = null;
            // ignoreDomainsFile = null;
            // textFields.scaleFigureTextField = '';
            // textFields.maxCutoffTextField = '';
            // textFields.cutoffTextField = '';
            // checkboxes.absoluteResultsCheckbox = false;
        }).catch(error => {
            console.log(error);
        });
    }

    return (
        <div className='protplot'>
            <h3>PropPlot page</h3>
            <p>
            </p>
            <div>
                <Grid container spacing={3} alignItems='center'>
                    <Grid item xs={12}>
                        <Paper className={classes.paper} variant='outlined'>Use Prodoplot by first uploading your fasta file, and then adding options if desired, and finally press the Go button!</Paper>
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='fastatxt' header='Fasta File' body='The file needs to contain fasta sequences in files named either .fa or .fasta.'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='fasta' handleFile={handleFastaFile} />
                    </Grid>
                    <Grid item xs={4}>
                        <AccordionSetup id='cutofftxt' header='Enter a number between 0 and 1.' body='Only domains occuring in a ratio higher than the number are plotted (e.g. If the value is 0.5, the domain has to occur somewhere in the protein of at least 50% of sequences).'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='cutoff' name='cutoffTextField' value={textFields.cutoffTextField} type='number' label='Cutoff' onChange={handleTextField} />
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='proteingroupstxt' header='(Optional) Protein Groups File:' body='A tab separated file that in the first column are the sequence headers, and in the second column are the names for the group that the sequence belongs to. This allows one to run all fasta sequences in one go, but then split the sequences and results into different groups of sequences, for example by grouping them into groups of sequences from different clades of organisms.'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='proteingroups' handleFile={handleProteinGroupsFile} color='default' />
                    </Grid>
                    <Grid item xs={4}>
                        <AccordionSetup id='max-cutofftxt' header='Enter a number between 0 and 1.' body='Only domains that have a maximum prevalence at a relative place in the protein group above this ratio are plotted (e.g. if value is 0.5, 50% of the sequences have to have this domain at the same relative position).'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='max-cutoff' name='maxCutoffTextField' value={textFields.maxCutoffTextField} type='number' label='Max Cutoff' onChange={handleTextField} />
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='colortxt' header='(Optional) Color File:' body='A tab separated file that has a list of domain names in the first column, and a list of the hexcodes (e.g. #fffff) in the second column. This is required if you want custom colors on your output graphs.'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='color' handleFile={handleColorFile} color='default' />
                    </Grid>
                    <Grid item xs={4}>
                        <AccordionSetup id='scale-figuretxt' header='Enter a number larger than 0.' body='The number you input represents the number of inches per 100pb that the plot is used to display.'></AccordionSetup>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='scale-figure' name='scaleFigureTextField' value={textFields.scaleFigureTextField} type='number' label='Scale Figure' onChange={handleTextField} />
                    </Grid>

                    <Grid item xs={4}>
                        <AccordionSetup id='ignoredomainstxt' header='(Optional) Ignore Domains File:' body='A tab separated file that in the first column has list of domain names that should be ignored when plotting.'></AccordionSetup>                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='ignoredomains' handleFile={handleIgnoreDomainsFile} color='default' />
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

                </Grid>
            </div>
        </div>
    );
}

export default ProtPlot;
