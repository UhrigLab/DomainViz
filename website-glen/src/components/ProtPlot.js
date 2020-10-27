import React, { useState } from 'react';
//import request from 'utils/Request'; TODO refactor to remove burden from ProtPlot.js
import axios from 'axios';
import UploadFile from './UploadFile';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { Button, Checkbox, FormControlLabel, TextField } from '@material-ui/core';


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
    const userID = guid();

    let fastaFile = null;

    let prositeFile = null;
    let pfamFile = null;
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
        fastaFile=file;
    }
    function handlePrositeFile(file) {
        prositeFile = file;
    }
    function handlePfamFile(file) {
        pfamFile = file;
    }
    function handleProteinGroupsFile(file) {
        proteinGroupsFile = file;
    }
    function handleColorFile(file) {
        colorFile = file;
    }
    function handleIgnoreDomainsFile(file) {
        ignoreDomainsFile = file;
    }


    async function sendPartOneFiles() {
        //Save file to server so the backend can access it
        if (fastaFile == null) {
            alert("Please upload a file before clicking go.");
            return;
        }
        const data = new FormData();
        data.append(userID, fastaFile, fastaFile.name)

        axios.post('/partonefiles', data, {
            headers: {
                'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
            },
            timeout: 3000,
        }).then(response => {
            console.log(response);
        })
        .catch(error => {
            console.log(error);
        });
    }
    async function sendPartTwoFiles() {
        const data = new FormData();
        //const absoluteResults = checkboxes.absoluteResultsCheckbox;
        //Save file to server so the backend can access it
        if (prositeFile == null) {
            alert("Please upload a prosite file before clicking go.");
            return;
        }
        if (pfamFile == null) {
            alert("Please upload a PFAM file before clicking go.");
            return;
        }
        if (proteinGroupsFile !== null) {
            data.append(userID, proteinGroupsFile, proteinGroupsFile.name);
        }
        if (colorFile !== null) {
            data.append(userID, colorFile, colorFile.name);
        }
        if (ignoreDomainsFile !== null) {
            data.append(userID, ignoreDomainsFile, ignoreDomainsFile.name);
        }
        if (checkboxes.absoluteResultsCheckbox) {
            console.log(checkboxes.absoluteResultsCheckbox.toString())
            data.append(checkboxes.absoluteResultsCheckbox.name, checkboxes.absoluteResultsCheckbox);
        }
        else {
            data.append(checkboxes.absoluteResultsCheckbox.name, checkboxes.absoluteResultsCheckbox);
        }
        if (textFields.cutoffTextField !== '') {
            if (parseFloat(textFields.cutoffTextField) < 0 || parseFloat(textFields.cutoffTextField) > 1) {
                alert("Please enter a valid cutoff value, or remove it.");
                return;
            }
            else {
                data.append(textFields.cutoffTextField.name, parseFloat(textFields.cutoffTextField));
            }
        }
        if (textFields.maxCutoffTextField !== '') {
            if (parseFloat(textFields.maxCutoffTextField) < 0 || parseFloat(textFields.maxCutoffTextField) > 1) {
                alert("Please enter a valid maximum cutoff value, or remove it.");
                return;
            }
            else {
                data.append(textFields.maxCutoffTextField.name, parseFloat(textFields.maxCutoffTextField));
            }
        }
        if (textFields.scaleFigureTextField !=='') {
            if (parseFloat(textFields.scaleFigureTextField) < 0) {
                alert("Please enter a valid figure scale value.");
                return;
            }
            else {
                data.append(textFields.scaleFigureTextField.name, parseFloat(textFields.scaleFigureTextField));
            }
        }
        data.append(userID, prositeFile, prositeFile.name);
        data.append(userID, pfamFile, pfamFile.name);

        

        axios.post('/parttwofiles', data, {
            headers: {
                'Content-Type': `multipart/form-data; boundary=${data._boundary}`,
            },
            timeout: 3000,
        }).then(response => {
            console.log(response);

            //reset values
            prositeFile=null;
            pfamFile=null;
            proteinGroupsFile=null;  
            colorFile=null;            
            ignoreDomainsFile=null;
            textFields.scaleFigureTextField='';
            textFields.maxCutoffTextField='';
            textFields.cutoffTextField='';
            checkboxes.absoluteResultsCheckbox=false;
            
        })
        .catch(error => {
            console.log(error);
        });
    }

    return (
        <div className='protplot'>
            <h3>PropPlot page</h3>
            <p>Instructions: Use propplot.py in a two step process, first call (prepare input for Prosite and PFAM):

                propplot.py collect Path/to/folder/containing/fasta/sequences OutputFilenameLead.fa

                This prepares the input files for both PFAM and Prosite.

                Follow the screen output to the webpages given to run your PFAM and Prosite run(s).

                Copy results from your mails into two single text files. One for all PFAM results and one for all Prosite results.

                python propplot.py collect /Users/myuser/propplotdata/data/ Testdata.today -w 0
                
                Second call (analyze Prosite and PFAM results and plot them)

                python propplot.py process Path/to/folder/containing/fasta/sequences OutputFilenameLead prosite Path/to/prositeresultfile
                                                    or
                python propplot.py process Path/to/folder/containing/fasta/sequences OutputFilenameLead pfam Path/to/pfamresultfile
                                                    or
                python propplot.py process Path/to/folder/containing/fasta/sequences OutputFilenameLead prosite Path/to/prositeresultfile pfam Path/to/pfamresultfile
                
                order of pfam / prosite is unimportant, but at least one option must be given.

                Example call:
                
                python propplot.py process /Users/myuser/propplotdata/data/ Testdata.today prosite Path/to/prositeresultfile' 
                </p>
            <div>
                <Grid container spacing={3} alignItems='center'>
                    <Grid item xs={6}>
                        <Paper className={classes.paper} variant='outlined'>Step 1</Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper} variant='outlined'>Step 2</Paper>
                    </Grid>
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Fasta File: The file needs to contain fasta sequences in files named either .fa or .fasta.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='fasta' handleFile={handleFastaFile}/>
                    </Grid>
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Prosite File: The file comes from Prosite, and must be in the table format.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='prosite' handleFile={handlePrositeFile} />
                    </Grid>
                    <Grid item xs={6}> {/* Go button for Step 1 */}
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={sendPartOneFiles}>
                            Go
                        </Button>
                    </Grid>
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>PFAM File: The file comes from PFAM, and must be in the table format.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='pfam' handleFile={handlePfamFile} />
                    </Grid>
                    <Grid item xs={6} />{/* These empty grids are here to fill the column without showing anything that doesnt need to be there */}
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>(Optional) Protein Groups File: A tab separated file that in the first column are the sequence headers, and in the second column are the names for the group that the sequence belongs to. 
                        This allows one to run all fasta sequences in one go, but then split the sequences and results into different groups of sequences, for example by grouping them into groups of sequences from different clades of organisms.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='proteingroups' handleFile={handleProteinGroupsFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>(Optional) Color File: A tab separated file that in the first column has a list of domain names with hexcodes (e.g. #fffff), and in the second column ######ASK_PASCAL what the rest means####### to have custom coloring.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='color' handleFile={handleColorFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>(Optional) Ignore Domains File: A tab separated file that in the first column has list of domain names that should be ignored when plotting.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile value='ignoredomains' handleFile={handleIgnoreDomainsFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Check the box to plot absolute numbers on y axis of plots instead of relative ones.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <FormControlLabel
                            control={<Checkbox checked={checkboxes.absoluteResultsCheckbox} onChange={handleCheckBox} name="absoluteResultsCheckbox" />}
                            label="AbsoluteResults?"
                        />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Enter a number between 0 and 1. Only domains occuring in a ratio higher than the number are plotted (e.g. If the value is 0.5, the domain has to occur somewhere in the protein of at least 50% of sequences).</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='cutoff' name='cutoffTextField' value={textFields.cutoffTextField} type='number' label='Cutoff' onChange={handleTextField}/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Enter a number between 0 and 1. Only domains that have a maximum prevalence at a relative place in the protein group above this ratio are plotted (e.g. if value is 0.5, 50% of the sequences have to have this domain at the same relative position).</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='max-cutoff' name='maxCutoffTextField' value={textFields.maxCutoffTextField} type='number' label='Max Cutoff' onChange={handleTextField}/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Enter a number larger than 0. Represents the number of inches per 100pb that the plot is used to display.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='scale-figure' name='scaleFigureTextField' value={textFields.scaleFigureTextField} type='number' label='Scale Figure' onChange={handleTextField}/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}> {/* Go button for step 2 */}
                        <Button variant='contained' color='primary' component='span' className={classes.button} onClick={sendPartTwoFiles}>
                            Go
                        </Button>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}

export default ProtPlot;