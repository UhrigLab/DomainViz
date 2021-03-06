import { React } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Button, Paper, Accordion, AccordionSummary, AccordionDetails, Divider } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
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
    column: {
        flexBasis: '50%',
    },
    divider: {
        backgroundColor: 'black',
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
                        {(index % 6 === 0) && //For 2 pdfs in a single row, 6 pdfs per group
                        <Grid item xs={12}>
                        <Accordion defaultExpanded={index==0} className={classes.accordion}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                                <Typography variant="h5">Group: {groupNames[index/6]}</Typography>
                                
                            </AccordionSummary>
                            <AccordionDetails>
                                <div className={classes.column}>
                                    <PDF pdf={images[index].file}/>
                                    <PDF pdf={images[index+2].file}/>
                                    <PDF pdf={images[index+4].file}/>
                                </div>
                                <div className={classes.column}>
                                    <PDF pdf={images[index+1].file}/>
                                    <PDF pdf={images[index+3].file}/>
                                    <PDF pdf={images[index+5].file}/>
                                </div>
                            </AccordionDetails>
                            {/* {(index % 3 === 0) && // For 3 pdfs in a row, 3 pdfs per group
                                <Grid item xs={12} alignItems='center'>
                                        <Paper className={classes.paper} variant='outlined'>
                                            <Typography variant="h5">Group: {groupNames[index/3]}</Typography>
                                        </Paper>
                                </Grid>
                            }
                            <Grid item xs={4}>
                                <PDF pdf={image.file}></PDF>
                            </Grid> */}
                            {/* {(index % 6 === 0) && //For 2 pdfs in a single row, 6 pdfs per group
                                <Grid item xs={12} alignItems='center'>
                                        <Paper className={classes.paper} variant='outlined'>
                                            <Typography variant="h5">Group: {groupNames[index/6]}</Typography>
                                        </Paper>
                                </Grid>
                            } */}
                            {/* <Grid item xs={6}>
                                <PDF pdf={image.file}></PDF>
                            </Grid> */}
                        </Accordion>
                        </Grid>
                        }
                        </>
                )
            })}
            <Grid item xs={12}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={gotoDownload}>Download</Button>
            </Grid>
        </>
    );
}