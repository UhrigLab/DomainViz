import { React, useEffect, useState } from 'react';
import { PDF } from './PDF';
import { Typography, Grid, Button, Paper, Accordion, AccordionSummary, AccordionDetails, Divider } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import { saveAs } from 'file-saver';
import { groupsize } from '../ViewPDF'

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
        // const [htmls, setHTMLs] = useState(["http://localhost:3000/api/iframes/b8bc8f46.3c3d.0ae4.9d56.54c3f17ce322_single_test_file_combined.html","http://localhost:3000/api/iframes/b8bc8f46.3c3d.0ae4.9d56.54c3f17ce322_single_test_file_combined_stickfigure.html","http://localhost:3000/api/iframes/b8bc8f46.3c3d.0ae4.9d56.54c3f17ce322_single_test_file_pfam.html","http://localhost:3000/api/iframes/b8bc8f46.3c3d.0ae4.9d56.54c3f17ce322_single_test_file_pfam_stickfigure.html","http://localhost:3000/api/iframes/b8bc8f46.3c3d.0ae4.9d56.54c3f17ce322_single_test_file_prosite.html","http://localhost:3000/api/iframes/b8bc8f46.3c3d.0ae4.9d56.54c3f17ce322_single_test_file_prosite_stickfigure.html"])
        const [htmls, setHTMLs] = useState([])
        function gotoDownload() {
            fetch('/api/download/' + uid).then(response => {
                saveAs(response.url, 'DomainViz_results.zip')
            });
        }

        useEffect(() => {
            for (let i=0; i<images.length; i++) {
                fetch('/api/iframes/'+images[i]).then(response => {
                    setHTMLs(old => [...old, response.url]);
                })
            }
        }, [])

        return (
        <>
            {htmls.map((image, index) => {
                return (
                    <>
                        {(image) && groupNames[index/6] && (index % groupsize === 0) && //For 2 html files in a single row, 6 pdfs per group
                        <Grid item xs={12} key={index}>
                             {/* If there is only a single group, there will only be groupsize (6) htmls in total, 
                                and if this is the case, start with the accordion expanded, but if there are more than one
                                groups, then all of the accordions should be closed. */}
                            <Accordion defaultExpanded={images.length===groupsize} className={classes.accordion}>
                                <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                                    <Typography variant="h5">Group: {groupNames[index/6]}</Typography>
                                    
                                </AccordionSummary>
                                <AccordionDetails>
                                    <div className={classes.column}>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index]} height="525" width="100%" ></iframe>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+2]} height="525" width="100%" ></iframe>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+4]} height="525" width="100%" ></iframe>
                                    </div>
                                    <div className={classes.column}>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+1]} height="525" width="100%" ></iframe>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+3]} height="525" width="100%" ></iframe>
                                        <iframe id="igraph" scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+5]} height="525" width="100%" ></iframe>
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