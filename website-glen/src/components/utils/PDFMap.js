import { React } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Button } from '@material-ui/core';
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
export const PDFMap = ({ images, uid }) => {
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
                        {/* <Grid item xs={2}>
                            <Typography variant='h5'>{"Group " + (index / groupsize)}</Typography>
                        </Grid> */}
                        <Grid item xs={4}>
                            <PDF pdf={image.file}></PDF>
                        </Grid>
                    </>
                )
            })}
            <Grid item xs={12}>
                <Button variant='contained' color='primary' component='span' className={classes.button} onClick={gotoDownload}>Download</Button>
            </Grid>
            <Grid item xs={12}/>
        </>
    );
}