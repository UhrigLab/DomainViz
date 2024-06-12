import React, { useState } from 'react';
//import request from 'utils/Request'; TODO refactor DomainViz to remove burden from the component, since it already does too much
import axios from 'axios';
import UploadFile from './utils/UploadFile';
import AccordionSetup from './AccordionSetup';
import isFasta from './utils/ValidateFile';
import { FastaFileMap } from './utils/FastaFileMap';

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import { Button, Checkbox, Divider, FormControlLabel, TextField, Typography } from '@material-ui/core';
import { useHistory } from 'react-router';
import DomainVizIcon from './img/domainviz.png';
import { saveAs } from 'file-saver';


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
    divider: {
        scale: 1.5,
        backgroundColor: 'black',
    },
    img: {
        height: "122px",
        width: "293px"
    },
}));


//generates random id;
let guid = () => {
    let s4 = () => {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    //return id of format 'aaaaaaaa'.'aaaa'.'aaaa'.'aaaa'.'aaaaaaaaaaaa'
    return s4() + s4() + '.' + s4() + '.' + s4() + '.' + s4() + '.' + s4() + s4() + s4();
}


function ProtPlot() {
    /* This functional component contains the logic, as well as the UI for the DomainViz page. This is the page that allows
     * users to upload their fasta files, add their own settings, and produce the results. It also automatically redirects the user
     * to the correct output page.
     */

    //TODO This was supposed to be temp for production, and the Home page was supposed to be added, but it hasn't been done yet.
    function getImages() {
        let id = textFields.uidTextField;
        if (!id) {
            alert("Please enter a result ID.");
            return;
        }
        if (id.length !== 36) {
            alert("Please enter a valid result ID, this ID is the wrong length.");
            return;
        }
        if (id.match('^[a-z0-9.]*$') === null) {
            alert("Please enter a valid result ID, this ID has the wrong characters.")
            return;
        }
        let idSplit = id.split('.')
        if (idSplit.length !== 5 || idSplit[0].length !== 8 || idSplit[1].length !== 4 || idSplit[2].length !== 4 
            || idSplit[3].length !== 4 || idSplit[4].length !== 12) {
            alert("Please enter a valid result ID, this ID isn't formatted correctly.")
            return
        }
        history.push('/view-results/' + textFields.uidTextField);
    }
    //end of temp

    const classes = useStyles();
    const resultID = guid();
    const history = useHistory()

    // Input files
    const [fastaFiles, setFastaFiles] = useState([]);

    // User-defined parameters
    const [checkboxes, setCheckboxes] = useState({
        absoluteResultsCheckbox: false,
        fastaFileLoadedCheckbox: false,
        scaleFigureCheckbox: false,
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

    function downloadTestFastaFile() {
        fetch('/api/testFasta').then(response => {
            saveAs(response.url);
        });
    }

    function uploadTestFastaFile() {
        // This function sends dummy info to the backend, so that it knows which file to use
        setFastaFiles(
            [ {file: "single_test", name: "single_test_file.fa"} ]
        )
    }
    function uploadMultipleTestFastaFiles() {
        // This function sends dummy info to the backend, so that it knows which files to use
        setFastaFiles(
            [
                {file: "mult_test_1", name: "multi_test_file_1.fa"},
                {file: "mult_test_2", name: "multi_test_file_2.fa"},
                {file: "mult_test_3", name: "multi_test_file_3.fa"},
            ]
        )
    }
    function clearFastaFile(index) {
        // Remove the fasta file at a certain index, or if there is no index given, clear all files
        if (typeof(index)=='number') {
            setFastaFiles([
                ...fastaFiles.slice(0, index),
                ...fastaFiles.slice(index+1)
            ]);
        }
        else {
            setFastaFiles([])
        }
    }
    function changeFAFileName(index, newName) {
        // If the fastafile is one of the example files, we only replace its name, otherwise, we replace the whole file
        // since that is the only way to change a File's name in Javascript. 
        if (fastaFiles[index].file) {
            if (fastaFiles[index].file.includes("test")) {
                setFastaFiles(
                    [
                        ...fastaFiles.slice(0, index),
                        {file: fastaFiles[index].file, name: newName + '.fa'},
                        ...fastaFiles.slice(index+1)
                    ]
                );
            }
        }
        else {
            let newFAFile = new File([fastaFiles[index]], newName + ".fa");
            setFastaFiles([
                ...fastaFiles.slice(0, index),
                newFAFile,
                ...fastaFiles.slice(index+1)
            ]);
        }
    }

    async function handleFastaFiles(fileList) {
        /* This function is run when the user uploads one or more fasta files, it validates the files
         * and stores them in the fastaFile State variable to send them to the backend.
         */
        // Check that there are no test files in the fastaFiles list, since the backend cannot currently handle both test and regular files
        for (let i=0; i<fastaFiles.length; i++) {
            if (fastaFiles[i].file) {
                if (fastaFiles[i].file.includes("test")) {
                    alert("Please remove all test files before uploading fasta files.");
                    return;
                }
            }
        }

        let files = []
        for (let i=0; i<fileList.length; i++) {
            files.push(fileList[i]);
        }
        if ((files.length + fastaFiles.length) >= 20) {
            alert("Please restrict your number of files to a maximum of 20 total.");
            return;
        }
        const promises = files.map(async file => {
            //Validate fastaFiles
            let valid = true;
            
            // Check the file's size
            if (((file.size / 1024) / 1024).toFixed(4) > 10) {
                alert("Your fasta file is greater than 10mb, which is the maximum allowed size.")
                valid = false;
            }
            // Check that the file is a fasta file
            await isFasta(file).then((result) => {
                valid = result;
            });

            return valid;
        })
        const validList = await Promise.all(promises);

        let filenames = ""
        for (let i=0; i<files.length; i++) {
            if(validList[i] === false) {
                return;
            }
            filenames = filenames + files[i].name + " "
        }
        alert("Successfully uploaded file(s): " + filenames)
        setFastaFiles(oldFaFiles => [...oldFaFiles, ...files])
    }

    async function sendPartOneFiles() {
        /* This function performs some final validation to the fasta files, and sends those files to the backend.
         * It's run when the user presses the "Submit Task" button.
         */
        //Save file to server so the backend can access it 
        const data = new FormData();

        if (fastaFiles.length === 0) {
            alert("Please upload a fasta file before clicking \"Submit Task\".");
            return;
        }
        if (fastaFiles[0].file) {
            if (fastaFiles[0].file.includes("test")) {
                // This means we are using the example file, or the example file list. 
                // There may be one or more files, and we append the name and the "file" object for each one, which here is either
                // single_test or mult_test_X.
                // Otherwise the entries become unaccessible in the backend, since the data is stored in a dictionary with the
                // first value being the key.
                data.append("result_id", resultID)
                for (let i=0; i<fastaFiles.length; i++) { 
                    data.append(fastaFiles[i].file, fastaFiles[i].name);
                }
            }
        }
        else {
            for (let i=0; i<fastaFiles.length; i++) {
                data.append(fastaFiles[i].name, fastaFiles[i], resultID);
            }
        }

        // Add optional settings
        if (checkboxes.absoluteResultsCheckbox) {
            data.append('absoluteResults', checkboxes.absoluteResultsCheckbox);
        }
        else {
            data.append('absoluteResults', checkboxes.absoluteResultsCheckbox);
        }
        if (textFields.cutoffTextField !== '') {
            if (parseFloat(textFields.cutoffTextField) < 0 || parseFloat(textFields.cutoffTextField) > 1) {
                alert("Please enter a valid minimum domain prevalence value, or remove it.");
                return;
            }
            else {
                data.append('cutoff', parseFloat(textFields.cutoffTextField));
            }
        }
        if (textFields.maxCutoffTextField !== '') {
            if (parseFloat(textFields.maxCutoffTextField) < 0 || parseFloat(textFields.maxCutoffTextField) > 1) {
                alert("Please enter a valid minimum domain position conservation value, or remove it.");
                return;
            }
            else {
                data.append('maxCutoff', parseFloat(textFields.maxCutoffTextField));
            }
        }
        if (textFields.scaleFigureTextField !== '') {
            if (parseFloat(textFields.scaleFigureTextField) < 0 || parseFloat(textFields.scaleFigureTextField) > 10) {
                alert("Please enter a valid figure scaling value.");
                return;
            }
            else {
                data.append('scaleFigure', parseFloat(textFields.scaleFigureTextField));
            }
        }

        // Make POST request to send the form-data object to the backend
        await axios.post('/api/sendfiles', data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        }).then(response => {
            // Reset setting values
            textFields.scaleFigureTextField = '';
            textFields.maxCutoffTextField = '';
            textFields.cutoffTextField = '';
            checkboxes.absoluteResultsCheckbox = false;
            history.push("/view-results/" + resultID);
        }).catch(error => {
            console.log(error);
            alert("Oh dear. Something has gone wrong. The following error has occured: " + error);
        });
    }

    return (
        <div className='protplot'>
            <Grid className={classes.root} container spacing={3} alignItems='center' justify='center' style={{marginTop: '90px'}}>
                <Grid item xs={12}>
                    <img src={DomainVizIcon} alt="DomainViz logo" className={classes.img}></img>
                </Grid>

                <Grid item xs={12}>
                    <Paper className={classes.paper} variant='outlined'>
                        <Typography variant='h5'>Protein domain search {'&'} visualization tool</Typography>
                        <Typography variant='body1'>Use DomainViz by first uploading one or more protein Fasta file(s), changing any options as desired and clicking "Submit Task".</Typography>
                    </Paper>
                </Grid>

                <Grid item xs={2} />
                <Grid item xs={3}>
                    <AccordionSetup id='fastatxt' header='Fasta File(s)' body='The file(s) need to contain fasta sequences in files named either .fa or .fasta.'></AccordionSetup>
                </Grid>
                <Grid item xs={2}>
                    <UploadFile value='fasta' handleFile={handleFastaFiles} acceptedTypes='.fa,.fasta' multiple={true} />
                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={clearFastaFile} style={{ marginLeft: "10px" }}>Clear All</Button>
                </Grid>
                <Grid item xs={1}>
                    <Checkbox disabled style={{ color: 'green' }} checked={(fastaFiles.length === 0) ? false : true} name="fastaFileLoadedCheckbox" />
                </Grid>

                <Grid item xs={12}>
                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={uploadTestFastaFile}>Load Single Example</Button>
                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={uploadMultipleTestFastaFiles} style={{ marginLeft: "10px" }}>Load Multiple Examples</Button>
                </Grid>

                <Grid item xs={12} >
                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={downloadTestFastaFile}>Download Examples</Button>
                </Grid>

                <FastaFileMap fastaFiles={fastaFiles} changeName={changeFAFileName} removeFile={clearFastaFile}></FastaFileMap>

                <Grid item xs={12}/>

                <Grid item xs={12}>
                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={sendPartOneFiles}>
                        Submit Task
                    </Button>
                </Grid>

                <Grid item xs={3}/>
                <Grid item xs={6}>
                    <Divider className={classes.divider}></Divider>
                </Grid>
                <Grid item xs={3}/>

                <Grid item xs={3}>
                    <AccordionSetup id='cutofftxt' header='Minimum domain prevalence' body='Enter a number between 0 and 1. The default value is 0.05. Only domains occuring in a ratio higher than the number are plotted (e.g. If the value is 0.5, the domain has to occur somewhere in the protein of at least 50% of sequences).'></AccordionSetup>
                </Grid>
                <Grid item xs={2}>
                    <TextField id='cutoff' name='cutoffTextField' value={textFields.cutoffTextField} type='number' inputProps={{ step: '0.01', max: 1, min: 0 }} onChange={handleTextField} />
                </Grid>

                <Grid item xs={3}>
                    <AccordionSetup id='max-cutofftxt' header='Minimum domain position conservation' body='Enter a number between 0 and 1. The default value is 0.05. Only domains that have a maximum prevalence at a relative place in the protein group above this ratio are plotted (e.g. if value is 0.5, 50% of the sequences have to have this domain at the same relative position).'></AccordionSetup>
                </Grid>
                <Grid item xs={2}>
                    <TextField id='max-cutoff' name='maxCutoffTextField' value={textFields.maxCutoffTextField} type='number' inputProps={{ step: '0.01', max: 1, min: 0 }} onChange={handleTextField} />
                </Grid>

                <Grid item xs={3}>
                    <AccordionSetup id='scale-figuretxt' header='Figure Scaling' body='This parameter is disabled by default. Click the checkbox to enable figure scaling. Enter a number between 0 and 10. The default value is 1, but this may not reflect well in your plots, and it is recommended that you leave it off. The number you input represents the number of inches per 100pb that the plot is used to display. Please note that visualizations on the server will not reflect figure scaling, but in the downloaded package, they will be.'></AccordionSetup>
                </Grid>
                <Grid item xs={1}>
                    <TextField disabled={(checkboxes.scaleFigureCheckbox) ? false : true} id='scale-figure' name='scaleFigureTextField' value={textFields.scaleFigureTextField} type='number' inputProps={{ min: 0, max: 10, step: '0.1' }} onChange={handleTextField} />
                </Grid>
                <Grid item xs={1}>
                    <FormControlLabel
                        control={<Checkbox checked={checkboxes.scaleFigureCheckbox} onChange={handleCheckBox} name="scaleFigureCheckbox" />}
                        label="Yes" />
                </Grid>

                <Grid item xs={3}>
                    <AccordionSetup id='absoluteresultstxt' header='Absolute y-axis?' body='Click the checkbox if you want absolute results on the y-axis. The default is no. Absolute results means that we will plot absolute numbers on y axis of plots instead of relative ones. If the box is unchecked, we plot relative results, if it is checked, we plot absolute results.'></AccordionSetup>
                </Grid>
                <Grid item xs={2}>
                    <FormControlLabel
                        control={<Checkbox checked={checkboxes.absoluteResultsCheckbox} onChange={handleCheckBox} name="absoluteResultsCheckbox" />}
                        label="Yes" />
                </Grid>

                <Grid item xs={6}>
                    <Divider className={classes.divider}></Divider>
                </Grid>

                {/* temp for production - should be added to Home component long-term. */}
                <Grid item xs={12} />
                <Grid item xs={12} />
                <Grid item xs={5}>
                    <Typography variant='body1'>Already have a code? Enter it here:</Typography>
                </Grid>
                <Grid item xs={3}>
                    <TextField fullWidth id='uid' name='uidTextField' value={textFields.uidTextField} label='Result ID' type="text" onChange={handleTextField} />
                </Grid>
                <Grid item xs={4}>
                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={getImages}>Go to my Results</Button>
                </Grid>
                {/* end of temp */}
            </Grid>
        </div>
    );
}

export default ProtPlot;
