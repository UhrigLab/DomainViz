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

function UploadFile({ value, handleFile, acceptedTypes=".tsv" }) {
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
        type="file"
        style={{ display: 'none' }}
        value={inputValue}
        onChange={e => returnFile(e.target.files[0])}
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
