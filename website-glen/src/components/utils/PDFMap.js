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
        console.log(images)

        return (
        <>
            {images.map((image, index) => {
                return (
                    <>
                        {image && (index % 6 === 0) && //For 2 pdfs in a single row, 6 pdfs per group
                        <Grid item xs={12}>
                             {/* If there is only a single group, there will only be 6 pdfs in total, 
                                and if this is the case, start with the accordion expanded, but if there are more than one
                                groups, then all of the accordions should be closed. */}
                            <Accordion defaultExpanded={images.length===6} className={classes.accordion}>
                                <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                                    <Typography variant="h5">Group: {groupNames[index/6]}</Typography>
                                    
                                </AccordionSummary>
                                <AccordionDetails>
                                    <div className={classes.column}>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={images[index]} height="525" width="100%" ></iframe>
                                        <p>{images[index]}</p>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={images[index+2]} height="525" width="100%" ></iframe>
                                        <p>{images[index+2]}</p>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={images[index+4]} height="525" width="100%" ></iframe>
                                        <p>{images[index+4]}</p>

                                        {/* <PDF pdf={images[index].file}/>
                                        <PDF pdf={images[index+2].file}/>
                                        <PDF pdf={images[index+4].file}/> */}
                                    </div>
                                    <div className={classes.column}>
                                    <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={images[index+1]} height="525" width="100%" ></iframe>
                                    <p>{images[index+1]}</p>
                                    <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={images[index+3]} height="525" width="100%" ></iframe>
                                    <p>{images[index+3]}</p>
                                    <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={images[index+5]} height="525" width="100%" ></iframe>
                                    <p>{images[index+5]}</p>
                                        {/* <PDF pdf={images[index+1].file}/>
                                        <PDF pdf={images[index+3].file}/>
                                        <PDF pdf={images[index+5].file}/> */}
                                    </div>
                                </AccordionDetails>
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