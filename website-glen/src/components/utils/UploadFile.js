import React, { useState } from 'react';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import { Button, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
      flexGrow: 1,
  },
  button: {
      padding: theme.spacing(1),
      textAlign: 'center',
  },
}));

function UploadFile({ value, handleFile, acceptedTypes=".tsv", multiple=false }) {
  /* This component is used to accept input files, do some simple validation, and perform a function call (handleFile)
   * after the completion of the upload. It may, or may not allow multiple file uploads, depending on the value of the `multiple` variable.
   */
  const classes = useStyles();
  const [inputValue, setInputValue] = useState("")
  const returnFile = (file) => {
    //reset the input's value so we can load another file
    setInputValue("")
    handleFile(file)
  }
  return (
    <>
      <input
        accept={acceptedTypes}
        className={classes.input}
        id={value}
        type='file'
        style={{ display: 'none' }}
        value={inputValue}
        onChange={e => returnFile(e.target.files)}
        multiple={ multiple }
      />
      <label htmlFor={value}>
        <Button
          variant="contained"
          color='default'
          component="span"
          startIcon={<CloudUploadIcon />}
          className={classes.button}>
          Upload
        </Button>
      </label>
    </>
  );
}

export default UploadFile;
