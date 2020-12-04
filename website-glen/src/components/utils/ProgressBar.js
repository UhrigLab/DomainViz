import { React } from 'react';
import { Typography, Grid, Paper, CircularProgress } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
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
export const ProgressBar = ({ progress }) => {
    const classes = useStyles()

    return (
        <>
            <Grid item xs={12}>
                <Paper className={classes.paper} variant='outlined' style={{marginTop: "70px"}}>                
                    <Typography variant='h5'>Loading, this may take a while, please wait...</Typography>
                </Paper>
            </Grid>
            <Grid item xs={12}>
                <CircularProgress variant='static' value={progress*20} style={{marginTop: "70px"}}></CircularProgress>
            </Grid>
        </>
    );
}