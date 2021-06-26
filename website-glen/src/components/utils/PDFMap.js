import { Fragment, React, useEffect, useState } from 'react';
import { Typography, Grid, Button, Accordion, AccordionSummary, AccordionDetails } from '@material-ui/core';
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
        const [htmls, setHTMLs] = useState([])
        function gotoDownload() {
            fetch('/api/download/' + uid).then(response => {
                saveAs(response.url, 'DomainViz_results.zip')
            });
        }

        // NOTE: There may be a warning in the console about this useEffect such as:
        // " Line 45:12:  React Hook useEffect has missing dependencies: 'htmls.length' and 'images'.
        // Either include them or remove the dependency array  react-hooks/exhaustive-deps"
        //
        // HOWEVER, do not add these, as there is asyncronous code running that will cause the same html file to be fetched
        // multiple times, rather than fetching all num_groups*groupsize. I realize that this is likely poor practices, however,
        // we are pressed for time and i cannot determine a solution that is better. 
        useEffect(() => {
            for (let i=0; i<images.length; i++) {
                fetch('/api/iframes/'+images[i]).then(response => {
                    if (htmls.length < images.length) //shouldnt add more htmls if we already have the same amount as we have image links
                        setHTMLs(old => [...old, response.url].sort());
                })
            }
        // eslint-disable-next-line
        }, []);

        return (
        <>
            <Grid item xs={12}>
                <Button variant='contained' color='default' component='span' className={classes.button} onClick={gotoDownload}>Download</Button>
            </Grid>
            {htmls.map((link, index) => {
                return (
                    <Fragment key={index}>
                        {(htmls.length % groupsize === 0) && (link) && groupNames[index/groupsize] && (index % groupsize === 0) && //For 2 html files in a single row, 6 html files per group
                        <Grid item xs={12}>
                             {/* If there is only a single group, there will only be groupsize (6) htmls in total, 
                                and if this is the case, start with the accordion expanded, but if there are more than one
                                groups, then all of the accordions should be closed. */}
                            <Accordion defaultExpanded={images.length === groupsize} className={classes.accordion}>
                                <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                                    <Typography variant="h5">Group: {groupNames[index / groupsize]}</Typography>
                                    
                                </AccordionSummary>
                                <AccordionDetails>
                                    <div className={classes.column}>
                                        <iframe id="igraph" title={htmls[index].split("/")[0]} scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index]} height="525" width="100%" />
                                        <iframe id="igraph" title={htmls[index+2].split("/")[0]} scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+2]} height="525" width="100%" />
                                        <iframe id="igraph" title={htmls[index+4].split("/")[0]} scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+4]} height="525" width="100%" />
                                    </div>
                                    <div className={classes.column}>
                                        <iframe id="igraph" title={htmls[index+1].split("/")[0]} scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+1]} height="525" width="100%" />
                                        <iframe id="igraph" title={htmls[index+3].split("/")[0]} scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+3]} height="525" width="100%" />
                                        <iframe id="igraph" title={htmls[index+5].split("/")[0]} scrolling="no" style={{border:"none"}} seamless="seamless" src={htmls[index+5]} height="525" width="100%" />
                                    </div>
                                </AccordionDetails>
                            </Accordion>
                        </Grid>
                        }
                    </Fragment>
                )
            })}
        </>
    );
}