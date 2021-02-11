import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Button, Checkbox, Divider, Grid, Paper, TextField, Typography } from '@material-ui/core';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

import { isFileFasta, isStringFasta } from './utils/ValidateInputs';
import { downloadTestFastaFile } from './utils/HTTPRequests';
import AccordionSetup from './AccordionSetup';
import UploadFile from './UploadFile';


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

  const [fastaFile, setFastaFile] = useState(null);
  const [textFields, setTextFields] = useState({
    centralCharTextField: '',
    widthTextField: '13',
    occurrencesTextField: '20',
    significanceTextField: '0.0000001',
    backgroundTextField: 'IPI Arabidopsis Proteome',
    fastaTextField: '',
  });
  const handleTextField = (event) => {
    setTextFields({ ...textFields, [event.target.name]: event.target.value })
  }

  const [fastaCheckbox, setFastaCheckbox] = useState(false);
  const handleFastaCheckbox = (event) => {
    setFastaCheckbox(event.target.checked);
  }
  const [foregroundRadio, setForgroundRadio] = useState('fasta');
  const handleForegroundRadio = (event) => {
    setForgroundRadio(event.target.value);
  };
  function uploadTestFastaFile() {
      // This function sends dummy info to the backend, so that it knows which file to use
      setFastaFile({
          file: "test",
          name: "test"
      });
  }
  function clearFastaFile() {
    // TODO Make clear button clear textfield as well
      setFastaFile(null);
      setTextFields({...textFields, [textFields.fastaTextField]: ''})
  }
  async function handleFastaFile(file) {
    //Validate fastaFile:
    let valid = true;

    // Check that the file is a fasta file
    await isFileFasta(file).then((result) => {
        valid = result;
    });

    if (valid) {
        setFastaFile(file);
        alert("Sucessfully uploaded file: " + file.name)
    }
    else {
        return;
    }
  }
  async function validateFastaText() {
    alert(textFields.fastaTextField)
    let valid = true;
    await isStringFasta(textFields.fastaTextField).then((result) => {
        valid = result;
    });
    if (valid) {
        setFastaFile({
            file: textFields.fastaTextField,
            name: "manual"
        });
    }
    else {
        return;
    }
    alert("Text accepted as fasta file.")
  }

  function sendUMotifFiles() {
    alert("Yay!, we did U-Motif!")
  }

  return (
    <Grid className={classes.root} container spacing={3} alignItems='center' justify='center'style={{marginTop: "90px"}} >
      
      <Grid item xs={12}>
        <Paper className={classes.paper} variant='outlined'>
            <Typography variant='h5'>Motif search {'&'} visualization tool</Typography>
            <Typography variant='body1'>Use U-Motif by first uploading a protein Fasta file, changing any options as desired and clicking "Submit Task".</Typography>
        </Paper>
      </Grid>

      <Grid item xs={2} />
      <Grid item xs={3}>
          <AccordionSetup id='fastatxt' header='Fasta File' body='The file needs to contain fasta sequences in files named either .fa or .fasta.'></AccordionSetup>
      </Grid>
      <Grid item xs={2}>
          <UploadFile value='fasta' handleFile={handleFastaFile} acceptedTypes='.fa,.fasta' />
          <Button variant='contained' color='default' component='span' className={classes.button} onClick={uploadTestFastaFile} style={{ marginLeft: "10px" }}>Load Example</Button>
      </Grid>
      <Grid item xs={1}>
          <Button variant='contained' color='default' component='span' className={classes.button} onClick={clearFastaFile} >Clear File</Button>
      </Grid>
      <Grid item xs={1}>
          <Checkbox disabled style={{ color: 'green' }} checked={(fastaFile == null) ? false : true} name="fastaFileLoadedCheckbox" />
      </Grid>
      <Grid item xs={3}/>

      <Grid item xs={2}/>
      <Grid item xs={6} >
          <TextField id="fasta-textfield"  name='fastaTextField' label="Fasta File" placeholder="Paste Text Here" multiline fullWidth rowsMax={5} variant='outlined' value={textFields.fastaTextField} onChange={handleTextField} />
      </Grid>
      <Grid item xs={1}>
          <Button variant='contained' color='default' component='span' className={classes.button} onClick={validateFastaText} >Validate Text</Button>
      </Grid>
      <Grid item xs={3}/>

      <Grid item xs={2} />
      <Grid item xs={6}>
          <Button variant='contained' color='default' component='span' className={classes.button} onClick={downloadTestFastaFile}>Download Example</Button>
      </Grid>
      <Grid item xs={4}/>

      <Grid item xs={12}>
        <FormControl component="fieldset">
          <FormLabel component="legend">Foreground Format:</FormLabel>
          <RadioGroup row aria-label="foreground" name="foregroundRadioGroup" value={foregroundRadio} onChange={handleForegroundRadio}>
            <FormControlLabel value="fasta" control={<Radio />} label="Fasta" />
            <FormControlLabel value="pre-aligned" control={<Radio />} label="Pre-Aligned" />
            <FormControlLabel value="text" control={<Radio />} label="Text" />
          </RadioGroup>
        </FormControl>
      </Grid>


      <Grid item xs={6}>
        <Divider className={classes.divider}></Divider>
      </Grid>

      <Grid item xs={12}/>

      <Grid item xs={3}>
        <AccordionSetup id='centralchartxt' header='Central Character' body='Detailed Description'></AccordionSetup>
      </Grid>
      <Grid item xs={2}>
          <TextField id='centralchar' name='centralCharTextField' value={textFields.centralCharTextField} type='text' inputProps={{ maxlength: "1" }} onChange={handleTextField}/>
      </Grid>
      <Grid item xs={3}>
        <AccordionSetup id='widthtxt' header='Width' body='Detailed Description'></AccordionSetup>
      </Grid>
      <Grid item xs={2}>
          <TextField id='width' name='widthTextField' value={textFields.widthTextField} type='number' inputProps={{ min: 3, max: 35, step: 2 }} onChange={handleTextField}/>
      </Grid>

      <Grid item xs={3}>
        <AccordionSetup id='occurrencestxt' header='Occurrences' body='Detailed Description'></AccordionSetup>
      </Grid>
      <Grid item xs={2}>
          <TextField id='occurrences' name='occurrencesTextField' value={textFields.occurrencesTextField} type='number' onChange={handleTextField}/>
      </Grid>
      <Grid item xs={3}>
        <AccordionSetup id='significancetxt' header='Significance' body='Detailed Description'></AccordionSetup>
      </Grid>
      <Grid item xs={2}>
          <TextField id='significance' name='significanceTextField' value={textFields.significanceTextField} type='number' inputProps={{ min: 0, max: 0.000001, step: 0.0000001 }} onChange={handleTextField}/>
      </Grid>

      <Grid item xs={12}>
        <Button variant='contained' color='default' component='span' className={classes.button} onClick={sendUMotifFiles}>
            Submit Task
        </Button>
      </Grid>

    </Grid>
  );
}

export default MotifX;
