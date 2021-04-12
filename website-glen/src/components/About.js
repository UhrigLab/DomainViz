import React from 'react';
import { Grid, Paper, Typography, Link } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import {  Link as RouterLink } from 'react-router-dom';



const useStyles = makeStyles((theme) => ({
  paper: {
      padding: theme.spacing(2),
      textAlign: 'left',
      color: theme.palette.text.secondary,
  },
  link: {
    fontWeight: 'fontWeightBold',
    color: 'black',
    textDecoration: 'underline',
  },
  img: {
      width: '800px',
      height: '580px',
  },
}));
export const About = () => {
  const classes = useStyles()

  return (
      <Grid container spacing={3} alignItems='center' justify='center' style={{ marginTop: "90px" }}>
        <Grid item xs={11}>
          <Typography variant='h4'>About Us</Typography>

          <Paper className={classes.paper} variant='outlined' >
            <Typography variant='body1' display='inline'>The  </Typography>
            <Link className={classes.link} target='_blank' href='https://www.uhriglab.com/'>Uhrig Lab</Link> 
            <Typography variant='body1' display='inline'>  at the University of Alberta is a protein biochemistry and proteomics research group interested in protein function discovery. We are also currently developing multiple open-source, accessible, and easy to use protein sequence analysis tools to enable biological discovery.</Typography>
            <Typography paragraph/>

            <Typography variant='body1' paragraph>Despite the Uhrig Lab’s focus on plant proteins and proteomics, tools such as these are interdisciplinary and can assist a wide range of user groups interested in protein domain analysis. </Typography>

            <Typography variant='h6'>DomainViz</Typography>
            <Typography variant='body1'>The Uhrig Lab, working in conjunction with ETH collaborator Dr. Pascal Schläpfer; have developed DomainViz.</Typography>
            <Typography variant='body1' display='inline'>Our first tool,  </Typography>
            <RouterLink className={classes.link} to='/domainviz' underline='always' color='textSecondary'>DomainViz</RouterLink>
            <Typography variant='body1' display='inline'>  was created to assist molecular biological and biochemical researchers to easily inspect and visualize domain elements within single proteins or protein groups. DomainViz has the ability to be used as a discovery tool as well as a purely visualization tool for known, related protein sequences. For example, users can upload protein sequences of homologs from multiple species and visualize the extent to which particular protein domains are evolutionarily conserved. Alternatively, users can use DomainViz to visualize the degree of conservation of protein domains between members of a protein family in a single species. </Typography>
            <Typography paragraph/> 
            
          </Paper>
        </Grid>
      </Grid>
  );
}

