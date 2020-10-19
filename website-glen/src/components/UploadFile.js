import React, { useRef } from 'react';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import { Button, Grid, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  root: {
      flexGrow: 1,
  },
  button: {
      padding: theme.spacing(1),
      textAlign: 'center',
  },
}));

function UploadFile({ handleFile, text, color="primary" }) {
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
          color={color}
          component="span"
          startIcon={<AddCircleIcon />}
          className={classes.button}>
          {text}
        </Button>
      </label>
    </>
  );
}

export default UploadFile;
