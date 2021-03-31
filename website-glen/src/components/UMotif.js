import React, { useState } from 'react';
import axios from 'axios';

import { makeStyles } from '@material-ui/core/styles';
import { Button, Checkbox, Divider, Grid, List, ListItem, ListItemText, ListSubheader, Paper, TextField, Typography } from '@material-ui/core';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

import { isFileFasta, isStringFasta } from './utils/ValidateInputs';
import { downloadTestFastaFile } from './utils/HTTPRequests';
import AccordionSetup from './AccordionSetup';
import UploadFile from './utils/UploadFile';
import { useHistory } from 'react-router';


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
    list: {
        backgroundColor: theme.palette.grey[200],
    },
    img: {
        height: "10x",
        width: "10px"
    },
    divider: {
        scale: 1.5,
        backgroundColor: 'black',
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
function MotifX() {
    const classes = useStyles();
    const resultID = guid();
    const history = useHistory();

    // States for user input + UI elements 
    const [fgFastaFiles, setFGFastaFiles] = useState([]);
    const [bgFastaFiles, setBGFastaFiles] = useState([]);
    const [textFields, setTextFields] = useState({
        fgCentralCharTextField: '',
        widthTextField: '13',
        occurrencesTextField: '20',
        significanceTextField: '0.0000001',
        fastaTextField: '',
        bgCentralCharTextField: '',
    });
    const handleTextField = (event) => {
        setTextFields({ ...textFields, [event.target.name]: event.target.value });
    }
    const [listSelectedIndex, setListSelectedIndex] = useState(0);
    const [bgListSelectedIndex, setBGListSelectedIndex] = useState(0);
    // Foreground variable is bool, says whether the list item was clicked for the foreground fasta file,
    // or background fasta file
    const handleListItemClick = (event, foreground, itemIndex) => {
        if (foreground) 
            setListSelectedIndex(itemIndex);
        else
            setBGListSelectedIndex(itemIndex);
    }
    const [foregroundRadio, setForgroundRadio] = useState('fasta');
    const handleForegroundRadio = (event) => {
        setForgroundRadio(event.target.value);
    };

    function uploadTestFastaFile() {
        // This function sends dummy info to the backend, so that it knows which file to use
        setFGFastaFiles(
            [ { file: "single_test", name: "test.fa"} ]
        );
    }
    function clearFastaFiles(foreground) {
        // TODO Make clear button clear textfield as well - currently doesnt update any textfield
        if (foreground) {
            setFGFastaFiles([]);
            textFields.fastaTextField = "";
        }
        else {
            setBGFastaFiles([]);
        }
    }
    async function handleFastaFiles(fileList) {       
        let files = []
        for (let i = 0; i < fileList.length; i++) {
            files.push(fileList[i])
        }
        if ((files.length + fgFastaFiles.length) > 1) {
            alert("Please restrict your foreground files to a maximum of 1 fasta file.");
            return;
        }
        const promises = files.map(async file => {
            //Validate fastaFiles
            let valid = true;

            // Check the file's size
            if (((file.size / 1024) / 1024).toFixed(4) > 100) {
                alert("Your fasta file is greater than 100mb, which is the maximum allowed size.")
                valid = false;
            }
            // // Check that the file is a fasta file
            await isFileFasta(file).then((result) => {
                valid = result;
            });

            return valid;
        })
        const validList = await Promise.all(promises);

        let filenames = ""
        for (let i = 0; i < files.length; i++) {
            if (validList[i] === false) {
                alert("File " + files[i].name + " is invalid")
                return;
            }
            filenames = filenames + files[i].name + " "
        }
        alert("Successfully uploaded file(s): " + filenames)
        setFGFastaFiles(oldFaFiles => [...oldFaFiles, ...files])
    }
    async function handleBGFastaFiles(fileList) {   
        let files = []
        for (let i = 0; i < fileList.length; i++) {
            files.push(fileList[i])
        }
        if ((files.length + bgFastaFiles.length) > 1) {
            alert("Please restrict your foreground files to a maximum of 1 fasta file.");
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
            // // Check that the file is a fasta file
            await isFileFasta(file).then((result) => {
                valid = result;
            });

            return valid;
        })
        const validList = await Promise.all(promises);

        let filenames = ""
        for (let i = 0; i < files.length; i++) {
            if (validList[i] === false) {
                alert("File " + files[i].name + " is invalid")
                return;
            }
            filenames = filenames + files[i].name + " "
        }
        alert("Successfully uploaded file(s): " + filenames)
        setBGFastaFiles(oldFaFiles => [...oldFaFiles, ...files])
    }
    async function validateFastaText() {
        alert(textFields.fastaTextField)
        let valid = true;
        await isStringFasta(textFields.fastaTextField).then((result) => {
            valid = result;
        });
        if (valid) {
            setFGFastaFiles(
                [{ file: textFields.fastaTextField, name: "manual.fa", type: "manual" }]
            );
        }
        else {
            return;
        }
        alert("Text accepted as fasta file.")
    }

    // This function sends the form to the backend
    async function sendUMotifFiles() {
        //send files and other data from the form via POST so the backend can access it 
        const data = new FormData();
        data.append("result_id", resultID)

        // Files
        if (fgFastaFiles.length === 0) {
            alert("Please upload a foreground fasta file before clicking \"Submit Task\".");
            return;
        }
        if (fgFastaFiles[0].file) {
            console.log("file[i].file exists")
            if (fgFastaFiles[0].file.includes("test")) {
                // This means we are using the example file, or the example file list. 
                // There may be one or more files, and we append the name and the "file" object for each one, which here is either
                // single_test or mult_test_X.
                // Otherwise the entries become unaccessible in the backend, since the data is stored in a dictionary with the
                // first value being the key.
                for (let i=0; i<fgFastaFiles.length; i++) { 
                    data.append(fgFastaFiles[i].file, fgFastaFiles[i].name);
                }
            }
            else if (fgFastaFiles[0].type) {
                if (fgFastaFiles[0].type.includes("manual")) {
                    // Here we append 2 different (key, value) pairs because we need the name, in case the user renamed the file,
                    // as well as the data as a string, and FormData() objects dont need
                    data.append("manual", fgFastaFiles[0].name);
                    data.append(fgFastaFiles[0].name, fgFastaFiles[0].file)
                }
                else 
                    alert("Something went wrong with your fasta text, we could not process it correctly.")
            }
            else {
                alert("Something went wrong with your fasta file.", fgFastaFiles[0]);
            }
        }
        else {
            console.log("adding manually")
            for (let i=0; i<fgFastaFiles.length; i++) {
                data.append(fgFastaFiles[i].name, fgFastaFiles[i], "foreground");
            }
        }
        switch (bgListSelectedIndex) {
            
            case 0:
                data.append("background", "arabidopsis");
                break;
            case 1:
                data.append("background", "human");
                break;
            case 2:
                // Only check background file if the user selected to upload it
                if (bgFastaFiles.length === 0) {
                    alert("Please upload a background fasta file, or select a different background from the list.");
                    return;
                }
                
                for (let i=0; i<bgFastaFiles.length; i++) {
                    data.append(bgFastaFiles[i].name, bgFastaFiles[i], "background");
                }
                break;
            default:
                data.append("background", "arabidopsis");
                break;
        }

        // Textfields
        if (textFields.bgCentralCharTextField !== '') {
            if (textFields.bgCentralCharTextField.length > 1) {
                alert("Your background central character should only have one entry.");
                return;
            }
            else
                data.append('bgCentralChar', textFields.bgCentralCharTextField);
        }
        if (textFields.fgCentralCharTextField !== '') {
            if (textFields.fgCentralCharTextField.length > 1) {
                alert("Your foreground central character should only have one entry.");
                return;
            }
            else
                data.append('fgCentralChar', textFields.fgCentralCharTextField);
        }
        if (textFields.occurrencesTextField !== '') {
            if (parseInt(textFields.occurrencesTextField) < 1) {
                alert("Please enter an occurences number that is greater than 0.");
                return;
            }
            else
                data.append('occurences', parseInt(textFields.occurrencesTextField));
        }
        if (textFields.significanceTextField !== '') {
            if (parseFloat(textFields.significanceTextField) <= 0) {
                alert("Please enter a significance value that is greater than 0.");
                return;
            }
            else
                data.append('significance', parseFloat(textFields.significanceTextField));
        }
        if (textFields.widthTextField !== '') {
            if (parseInt(textFields.widthTextField) < 3 || parseInt(textFields.widthTextField) > 35) {
                alert("Please enter an width number that is between 3 and 35.");
                return;
            }
            else if ((parseInt(textFields.widthTextField) % 2) === 0) {
                alert("Please enter an odd width number.");
                return;
            }
            else
                data.append('width', parseInt(textFields.widthTextField));
        }

        await axios.post('/api/u-motif', data, {
            headers: {
                'Content-Type': 'multipart/form-data',
            }
        }).then(response => {
            textFields.bgCentralCharTextField = '';
            textFields.fgCentralCharTextField = '';
            textFields.fastaTextField = '';
            textFields.occurrencesTextField = '20';
            textFields.significanceTextField = '0.0000001';
            textFields.widthTextField = '13';

            history.push("/view-umotif-results/" + resultID);
        }).catch(error => {
            console.log(error);
            alert("Oh dear. Something has gone wrong. The following error has occured: " + error);
        });
    }

    return (
        <Grid className={classes.root} container spacing={3} alignItems='center' justify='center' style={{ marginTop: "90px" }} >

            <Grid item xs={12}>
                <Paper className={classes.paper} variant='outlined'>
                    <Typography variant='h5'>Motif search {'&'} visualization tool</Typography>
                    <Typography variant='body1'>Use U-Motif by first uploading a protein Fasta file, changing any options as desired and clicking "Submit Task".</Typography>
                </Paper>
            </Grid>

            <Grid item xs={2} />
            <Grid item xs={3}>
                <AccordionSetup id='fastatxt' header='Foreground Fasta File' body='The file needs to contain fasta sequences in files named either .fa or .fasta.'></AccordionSetup>
            </Grid>
            <Grid item xs={2}>
                <UploadFile value='fasta' handleFile={handleFastaFiles} acceptedTypes='.fa,.fasta' />
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={uploadTestFastaFile} style={{ marginLeft: "10px" }}>Load Example</Button>
            </Grid>
            <Grid item xs={1}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={() => clearFastaFiles(true)} >Clear File</Button>
            </Grid>
            <Grid item xs={1}>
                <Checkbox disabled style={{ color: 'green' }} checked={(fgFastaFiles.length === 0) ? false : true} name="fastaFileLoadedCheckbox" />
            </Grid>
            <Grid item xs={3} />

            <Grid item xs={2} />
            <Grid item xs={6} >
                <TextField id="fasta-textfield" name='fastaTextField' label="Fasta File" placeholder="Paste Text Here" multiline fullWidth rowsMax={5} variant='outlined' value={textFields.fastaTextField} onChange={handleTextField} />
            </Grid>
            <Grid item xs={1}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={validateFastaText} >Validate Text</Button>
            </Grid>
            <Grid item xs={3} />

            <Grid item xs={2} />
            <Grid item xs={6}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={downloadTestFastaFile}>Download Example</Button>
            </Grid>
            <Grid item xs={2} />

            <Grid item xs={12}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={sendUMotifFiles}>
                    Submit Task
                </Button>
            </Grid>


            <Grid item xs={12}>
                <FormControl component="fieldset">
                    <FormLabel component="legend">Foreground Format:</FormLabel>
                    <RadioGroup row aria-label="foreground" name="foregroundRadioGroup" value={foregroundRadio} onChange={handleForegroundRadio}>
                        <FormControlLabel value="fasta" control={<Radio />} label="Fasta" />
                        <FormControlLabel value="pre-aligned" control={<Radio />} label="Pre-Aligned" />
                        <FormControlLabel value="text" control={<Radio />} label="Text" />
                        <FormControlLabel value="ms-ms" control={<Radio />} label="MS/MS" />
                        </RadioGroup>
                </FormControl>
            </Grid>
            {foregroundRadio === "ms-ms" &&
                <>
                <Grid item xs={5}/>
                <Grid item xs={2}>
                <List aria-labelledby="list-subheader"
                    className = {classes.list}
                    subheader = {
                        <ListSubheader id='list-subheader'>
                            Extend From:
                        </ListSubheader>
                    }    
                >
                    <ListItem 
                        selected={listSelectedIndex === 0}
                        onClick={(e) => handleListItemClick(e, true, 0)}    
                    >
                        <ListItemText>IPI Arabidopsis Proteome</ListItemText>
                    </ListItem>
                    <ListItem 
                        selected={listSelectedIndex === 1}
                        onClick={(e) => handleListItemClick(e, true, 1)}    
                    >
                        <ListItemText>IPI Human Proteome (Example)</ListItemText>
                    </ListItem>
                </List>
                </Grid>
                <Grid item xs={5}/>

                </>
            }


            <Grid item xs={6}>
                <Divider className={classes.divider}></Divider>
            </Grid>
            <Grid item xs={12} />

            <Grid item xs={3}>
                <AccordionSetup id='centralchartxt' header='Central Character' body='Detailed Description'></AccordionSetup>
            </Grid>
            <Grid item xs={2}>
                <TextField id='fgcentralchar' name='fgCentralCharTextField' value={textFields.fgCentralCharTextField} inputProps={{ maxLength: 1 }} onChange={handleTextField} />
            </Grid>
            <Grid item xs={3}>
                <AccordionSetup id='widthtxt' header='Width' body='Detailed Description'></AccordionSetup>
            </Grid>
            <Grid item xs={2}>
                <TextField id='width' name='widthTextField' value={textFields.widthTextField} type='number' inputProps={{ min: 3, max: 35, step: 2 }} onChange={handleTextField} />
            </Grid>

            <Grid item xs={3}>
                <AccordionSetup id='occurrencestxt' header='Occurrences' body='Detailed Description'></AccordionSetup>
            </Grid>
            <Grid item xs={2}>
                <TextField id='occurrences' name='occurrencesTextField' value={textFields.occurrencesTextField} type='number' inputProps={{ min: 1}} onChange={handleTextField} />
            </Grid>
            <Grid item xs={3}>
                <AccordionSetup id='significancetxt' header='Significance' body='Detailed Description'></AccordionSetup>
            </Grid>
            <Grid item xs={2}>
                <TextField id='significance' name='significanceTextField' value={textFields.significanceTextField} type='number' inputProps={{ min: 0, max: 0.000001, step: 0.0000001 }} onChange={handleTextField} />
            </Grid>

            <Grid item xs={5}/>
                <Grid item xs={2}>
                <List aria-labelledby="bg-list-subheader"
                    className = {classes.list}
                    subheader = {
                        <ListSubheader id='bg-list-subheader'>
                            Background
                        </ListSubheader>
                    }    
                >
                    <ListItem 
                        selected={bgListSelectedIndex === 0}
                        onClick={(e) => handleListItemClick(e, false, 0)}    
                    >
                        <ListItemText>IPI Arabidopsis Proteome</ListItemText>
                    </ListItem>
                    <ListItem 
                        selected={bgListSelectedIndex === 1}
                        onClick={(e) => handleListItemClick(e, false, 1)}    
                    >
                        <ListItemText>IPI Human Proteome (Example)</ListItemText>
                    </ListItem>
                    <ListItem 
                        selected={bgListSelectedIndex === 2}
                        onClick={(e) => handleListItemClick(e, false, 2)}    
                    >
                        <ListItemText>Upload (Advanced)</ListItemText>
                    </ListItem>
                </List>
            </Grid>
            <Grid item xs={5}/>
            
            {bgListSelectedIndex === 2 && // The user wants to upload a background file themselves
            <>
                <Grid item xs={3}>
                    <AccordionSetup id='fastatxt' header='Background Fasta File' body='The file needs to contain fasta sequences in files named either .fa or .fasta.'></AccordionSetup>
                </Grid>
                <Grid item xs={2}>
                    <UploadFile value='bg-fasta' handleFile={handleBGFastaFiles} acceptedTypes='.fa,.fasta' />
                </Grid>
                <Grid item xs={1}>
                    <Button variant='contained' color='default' component='span' className={classes.button} onClick={() => clearFastaFiles(false)} >Clear File</Button>
                </Grid>
                <Grid item xs={1}>
                    <Checkbox disabled style={{ color: 'green' }} checked={(bgFastaFiles.length === 0) ? false : true} name="bg-fastaFileLoadedCheckbox" />
                </Grid>
                <Grid item xs={3} />

                <Grid item xs={3}>
                    <AccordionSetup id='bg-centralchartxt' header='Background Central Character' body='Detailed Description'></AccordionSetup>
                </Grid>
                <Grid item xs={2}>
                    <TextField id='bg-centralChar' name='bgCentralCharTextField' value={textFields.bgCentralCharTextField} inputProps={{ maxLength: "1" }} onChange={handleTextField} />
                </Grid>
                <Grid item xs={5} />
            </>
            }
            

            <Grid item xs={12} />
        </Grid>
    );
}

export default MotifX;
