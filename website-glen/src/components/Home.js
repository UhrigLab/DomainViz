import React, { useState } from 'react';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import { Button, Checkbox, FormControlLabel, TextField } from '@material-ui/core';
import { useHistory } from 'react-router-dom';

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

function Home() {
  const classes = useStyles();
  let history = useHistory();

  const [textFields, setTextFields] = useState({
    uidTextField: '',
  });
  const handleTextField = (event) => {
    setTextFields({ ...textFields, [event.target.name]: event.target.value })
  }

  function getImages() {
    history.push('/view-results/' + textFields.uidTextField);
  }
  return (
    <>
      <h3>Home page</h3>
      <Grid container spacing={3} alignItems='center'>

        <Grid item xs={12}>
          <Paper className={classes.paper} variant='outlined'>Already have a code? Enter it here:</Paper>
        </Grid>
        <Grid item xs={6}>
          <TextField id='uid' name='uidTextField' value={textFields.uidTextField} label='User ID' type="text" onChange={handleTextField} />
        </Grid>

        <Grid item xs={6}>
          <Button variant='contained' color='primary' component='span' className={classes.button} onClick={getImages}>Go</Button>
        </Grid>

      </Grid>
    </>
  );
}

export default Home;
