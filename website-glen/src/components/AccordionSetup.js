import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Accordion from '@material-ui/core/Accordion';
import AccordionSummary from '@material-ui/core/AccordionSummary';
import AccordionDetails from '@material-ui/core/AccordionDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';

const useStyles = makeStyles((theme) => ({
  root: {
    width: '100%',
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightRegular,
  },
}));

function AccordionSetup({ id, header, body }) {
    const classes = useStyles();
    
    return (
        <>
            <Accordion>
                <AccordionSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls={id + "-content"}
                    id={id + "-header"}
                >
                    <Typography className={classes.heading}>{header}</Typography>
                </AccordionSummary>
                <AccordionDetails>
                    <Typography>
                        {body}
                    </Typography>
                </AccordionDetails>
            </Accordion>
        </>
    );
}

export default AccordionSetup;
