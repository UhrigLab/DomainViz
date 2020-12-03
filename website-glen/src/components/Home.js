import React, { useState } from 'react';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import { Button, TextField, Typography } from '@material-ui/core';
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
  function gotoProtplot() {
    history.push('/protplot');
  }
  
  return (
    <>
      <Grid container spacing={3} alignItems='center'>
        <Grid item xs={12}>
          <Paper className={classes.paper} variant='outlined' style={{marginTop: "70px"}}>
            <Typography variant='h6'>Welcome to DomainVis, Hosted by the University of Alberta.</Typography>
          </Paper>
        </Grid>

        <Grid item xs={5}>
          <Typography variant='body1'>Already have a code? Enter it here:</Typography>
        </Grid>
        <Grid item xs={1}>
          <TextField id='uid' name='uidTextField' value={textFields.uidTextField} label='User ID' type="text" onChange={handleTextField} />
        </Grid>
        <Grid item xs={6}>
          <Button variant='contained' color='primary' component='span' className={classes.button} onClick={getImages}>Go to my Results!</Button>
        </Grid>

        <Grid item xs={12}></Grid>
        <Grid item xs={6}>
          <Typography variant='body1'>Don't have a code? Click on the button to go to the DomainVis tool and get to work!</Typography>
        </Grid>
        <Grid item xs={6}>
          <Button variant='contained' color='primary' component='span' className={classes.button} onClick={gotoProtplot}>Go to DomainVis!</Button>
        </Grid>
      </Grid>
    </>
  );
}

export default Home;
