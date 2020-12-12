import React from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';


const useStyles = makeStyles((theme) => ({
  paper: {
      padding: theme.spacing(2),
      textAlign: 'center',
      color: theme.palette.text.secondary,
  },
}));
export const About = () => {
  const classes = useStyles()

  return (
      <Grid container spacing={3} alignItems='center' justify='center' style={{ marginTop: "90px" }}>
        <Grid item xs={6}>
          <Typography variant='h5'>About Us</Typography>
          <Paper className={classes.paper} variant='outlined' >
          The Uhrig lab is a protein biochemistry and proteomics group interested in protein function discovery. 
          Despite the Uhrig labs focus on plant proteins and proteomics, tools such as these are interdisciplinary 
          and can assist a wide range of user groups interested in protein domain analysis. DomainViz was created to 
          assist molecular biological and biochemical researchers to easily inspect and visualize domain elements 
          within single proteins or protein groups. DomainViz has the ability to be used as a discovery tool as 
          well as a purely visualization tool for known, related protein sequences. 
          </Paper>
        </Grid>
      </Grid>
  );
}

