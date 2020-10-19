import React, { useRef } from 'react';
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

function UploadFile({ handleFile }) {
  const classes = useStyles();

  const handleChange = e => {
    const fileUploaded = e.target.files[0];
    handleFile(fileUploaded);
  }

  return (
    <>
      <input
        accept=".tsv"
        className={classes.input}
        id="contained-button-file"
        type="file"
        style={{ display: 'none' }}
        onChange={handleChange}
      />
      <label htmlFor="contained-button-file">
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
