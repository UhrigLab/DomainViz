import React, { useRef, useState } from 'react';
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

    const [checkboxes, setCheckboxes] = useState({
        absoluteResultsCheckbox: false,
    });
    const handleCheckBox = (event) => {
        setCheckboxes({ ...checkboxes, [event.target.name]: event.target.checked });
    };


    async function handleFastaFile(file) {
        //Save file to server so the backend can access it
        const data = new FormData();
        data.append(userID, file, file.name)

        axios.post('/fastafiles', data, {
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
    function handlePrositeFile(file) {
        console.log(file)
    }
    function handlePfamFile(file) {
        console.log(file)
    }
    function handleProteinGroupsFile(file) {
        console.log(file)
    }
    function handleColorFile(file) {
        console.log(file)
    }
    function handleIgnoreDomainsFile(file) {
        console.log(file)
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
                        <UploadFile handleFile={handleFastaFile} />
                    </Grid>
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Prosite File: The file comes from Prosite, and must be in the table format.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile handleFile={handlePrositeFile} />
                    </Grid>
                    <Grid item xs={6}> {/* Go button for Step 1 */}
                        <Button variant='contained' color='primary' component='span' className={classes.button}>
                            Go
                        </Button>
                    </Grid>
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>PFAM File: The file comes from PFAM, and must be in the table format.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile handleFile={handlePfamFile} />
                    </Grid>
                    <Grid item xs={6} />{/* These empty grids are here to fill the column without showing anything that doesnt need to be there */}
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>(Optional) Protein Groups File: A tab separated file that in the first column are the sequence headers, and in the second column are the names for the group that the sequence belongs to. 
                        This allows one to run all fasta sequences in one go, but then split the sequences and results into different groups of sequences, for example by grouping them into groups of sequences from different clades of organisms.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile text="Protein Groups File" handleFile={handleProteinGroupsFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>(Optional) Handle Color File: A tab separated file that in the first column has a list of domain names with hexcodes (e.g. #fffff), and in the second column ######ASK_PASCAL what the rest means####### to have custom coloring.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile text="Color File" handleFile={handleColorFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>(Optional) Ignore Domains File: A tab separated file that in the first column has list of domain names that should be ignored when plotting.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <UploadFile handleFile={handleIgnoreDomainsFile} color='default' />
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
                        <TextField id='cutoff' type='number' label='Cutoff'/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Enter a number between 0 and 1. Only domains that have a maximum prevalence at a relative place in the protein group above this ratio are plotted (e.g. if value is 0.5, 50% of the sequences have to have this domain at the same relative position).</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='max-cutoff' type='number' label='Max Cutoff'/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={4}>
                        <Paper className={classes.paper} variant='outlined'>Enter a number larger than 0. Represents the number of inches per 100pb that the plot is used to display.</Paper>
                    </Grid>
                    <Grid item xs={2}>
                        <TextField id='scale-figure' type='number' label='Scale Figure'/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <Button variant='contained' color='primary' component='span' className={classes.button}>
                            Go
                        </Button>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}

export default ProtPlot;