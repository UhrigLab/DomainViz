import { React } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Button, Paper, Box } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import { saveAs } from 'file-saver';

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
export const PDFMap = ({ images, uid, groupNames }) => {
        const classes = useStyles()
        const groupsize = 3;

        function gotoDownload() {
            fetch('/api/download/' + uid).then(response => {
                saveAs(response.url, 'DomainViz_results.zip')
            });
        }

        return (
        <>
            {images.map((image, index) => {
                return (
                    <>
                        {(index % 3 === 0) &&
                            <Grid item xs={12} alignItems='center'>
                                    <Paper className={classes.paper} variant='outlined'>
                                        <Typography variant="h5">Group: {groupNames[index/3]}</Typography>
                                    </Paper>
                            </Grid>
                        }
                        <Grid item xs={4}>
                            <PDF pdf={image.file}></PDF>
                        </Grid>
                    </>
                )
            })}
            <Grid item xs={12}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={gotoDownload}>Download</Button>
            </Grid>
        </>
    );
}