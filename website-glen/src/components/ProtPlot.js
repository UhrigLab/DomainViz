import React, { useRef, useState } from 'react';
import UploadFile from './UploadFile';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { Button, Checkbox, FormControlLabel, TextField } from '@material-ui/core';
import AddCircleIcon from '@material-ui/icons/AddCircle';


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

function ProtPlot() {
    const classes = useStyles();

    const [checkboxes, setCheckboxes] = useState({
        groupFilesCheckbox: true,
        absoluteResultsCheckbox: true,
    });

    const handleCheckBox = (event) => {
        setCheckboxes({ ...checkboxes, [event.target.name]: event.target.checked });
    };
    function handleFastaFile(file) {
        console.log(file)
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
            <p>Instructions: Use this program ... FILL ME IN ... </p>
            <div>
                <Grid container spacing={3}>
                    <Grid item xs={6}>
                        <Paper className={classes.paper} variant='outlined'>Step 1</Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <Paper className={classes.paper} variant='outlined'>Step 2</Paper>
                    </Grid>
                    <Grid item xs={6}>
                        <UploadFile text="Fasta File" handleFile={handleFastaFile} />
                    </Grid>
                    <Grid item xs={6}>
                        <UploadFile text="Prosite File" handleFile={handlePrositeFile} />
                    </Grid>
                    <Grid item xs={6}> {/* Go button for Step 1 */}
                        <Button variant='contained' color='secondary' component='span' className={classes.button}>
                            Go
                        </Button>
                    </Grid>
                    <Grid item xs={6}>
                        <UploadFile text="Pfam File" handleFile={handlePfamFile} />
                    </Grid>
                    <Grid item xs={6} />{/* These empty grids are here to fill the column without showing anything that doesnt need to be there */}
                    <Grid item xs={6}>
                        <UploadFile text="Protein Groups File" handleFile={handleProteinGroupsFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <UploadFile text="Color File" handleFile={handleColorFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <UploadFile text="Ignore Domains File" handleFile={handleIgnoreDomainsFile} color='default' />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <FormControlLabel
                            control={<Checkbox checked={checkboxes.groupFilesCheckbox} onChange={handleCheckBox} name="groupFilesCheckbox" />}
                            label="Group Files?"
                        />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <FormControlLabel
                            control={<Checkbox checked={checkboxes.absoluteResultsCheckbox} onChange={handleCheckBox} name="absoluteResultsCheckbox" />}
                            label="AbsoluteResults?"
                        />
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <TextField id='cutoff' type='number' helperText='Enter a number between 0 and 1' label='Cutoff'/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <TextField id='max-cutoff' type='number' helperText='Enter a number between 0 and 1' label='Max Cutoff'/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <TextField id='scale-figure' type='number' helperText='Enter a number between greater than 0' label='Scale Figure'/>
                    </Grid>
                    <Grid item xs={6} />
                    <Grid item xs={6}>
                        <Button variant='contained' color='secondary' component='span' className={classes.button}>
                            Go
                        </Button>
                    </Grid>
                </Grid>
            </div>
        </div>
    );
}

export default ProtPlot;