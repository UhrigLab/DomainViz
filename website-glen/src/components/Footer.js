import React from 'react';
import { Typography, Grid, Container } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { Link } from 'react-router-dom';

import UalbertaLogo from './img/UA-SCI-1C-SOLID-REVERSE.png'


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
    button: {
        padding: theme.spacing(1),
        textAlign: 'center',
        textDecorationColor: 'white'
    },
  }));

function Footer () {
        const classes = useStyles();
        return (
            <Container className={classes.container} maxWidth="xl" disableGutters style={{ marginTop: "20px" }}>
                <Grid container spacing={0} alignItems='center' justify='center'>
                    <Grid item xs={2}>
                        <img src={UalbertaLogo} alt="University Of Alberta" className={classes.img}></img>
                    </Grid>
                    <Grid item xs={3}/>
                    <Grid item xs={2}>
                        <Link to='/terms-of-use' >
                            <Typography className={classes.typography} variant='body1'>Terms of Use</Typography>
                        </Link>
                        <Link to='/privacy-statement'>
                            <Typography className={classes.typography} variant='body1'>Privacy Statement</Typography>
                        </Link>
                    </Grid>
                    <Grid item xs={3}/>
                    <Grid item xs={2}>
                        <Typography className={classes.typography} variant='body1'>Contact:</Typography>
                            <a href={`mailto:protools@ualberta.ca?subject=DomainViz Help`}>
                                <Typography className={classes.typography} variant='body1'>protools@ualberta.ca</Typography>
                            </a>
                        <Typography className={classes.typography} variant='body1'>{'\u00A9'} 2020 The Uhrig Lab</Typography>
                    </Grid>
                    
                </Grid>
            </Container>
    );
}
export default Footer;
