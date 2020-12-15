import React from 'react';
import { Typography, Grid, Button, Container } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';

import UalbertaLogo from './svg/UA-SCI-1C-SOLID-REVERSE.png'

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    container: {
        backgroundColor: 'black',
        width: '100%',
        minHeight: "125px",
        postion: 'absolute',
        bottom: 0,
        left: 0,
    },
    typography: {
        color: 'white',
    },
    img: {
        height: "100px",
        width: "300px"
    },
  }));

export const Footer = () => {
        const classes = useStyles()

        return (
        <Container className={classes.container} maxWidth="xl" disableGutters style={{ marginTop: "20px" }}>
            <Grid container spacing={0} alignItems='center' justify='center'>
                <Grid item xs={6}>
                    <img src={UalbertaLogo} className={classes.img}></img>
                </Grid>
                <Grid item xs={6}>
                    <Typography className={classes.typography} variant='body1'>Contact:</Typography>
                    <a href={`mailto:PROtools@ualberta.ca?subject=DomainViz Help`}>
                        <Typography className={classes.typography} variant='body1'>PROtools@ualberta.ca</Typography>
                    </a>
                    <Typography className={classes.typography} variant='body1'>{'\u00A9'} 2020 The Uhrig Lab</Typography>
                </Grid>
            </Grid>
        </Container>
        
    );
}