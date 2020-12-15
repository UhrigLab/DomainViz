import React from 'react';
import { Typography, Grid, Button, Container } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { useHistory } from 'react-router';

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
    },
  }));

function Footer () {
        const classes = useStyles();
        const history = useHistory();

        function goToTermsOfUse() {
            history.push('/terms-of-use');
        }
        return (
        <Container className={classes.container} maxWidth="xl" disableGutters style={{ marginTop: "20px" }}>
            <Grid container spacing={0} alignItems='center' justify='center'>
                <Grid item xs={6}>
                    <img src={UalbertaLogo} className={classes.img}></img>
                </Grid>
                <Grid item xs={3}/>
                <Grid item xs={1}>
                    {/* <Button component='span' color="primary" className={classes.button} onClick={goToTermsOfUse}>Terms of Use</Button> */}
                </Grid>
                <Grid item xs={1}>
                    <Typography className={classes.typography} variant='body1'>Contact:</Typography>
                    <Button color='default' component='span' className={classes.button}>
                        <a href={`mailto:PROtools@ualberta.ca?subject=DomainViz Help`}>
                            <Typography className={classes.typography} variant='body1'>PROtools@ualberta.ca</Typography>
                        </a>
                    </Button>
                    <Typography className={classes.typography} variant='body1'>{'\u00A9'} 2020 The Uhrig Lab</Typography>
                </Grid>
                
            </Grid>
        </Container>
        
    );
}
export default Footer;
