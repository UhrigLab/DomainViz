import React, { useEffect } from 'react';
import { Grid, Paper, Typography } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import ReactGA from 'react-ga';
import { createBrowserHistory } from 'history';


const useStyles = makeStyles((theme) => ({
  paper: {
      padding: theme.spacing(2),
      textAlign: 'left',
      color: theme.palette.text.secondary,
  },
  link: {
    fontWeight: 'fontWeightBold',
    color: 'black',
    textDecoration: 'underline',
  },
}));

const browserHistory = createBrowserHistory();
export const PrivacyStatement = () => {
  const classes = useStyles()

  useEffect(() => {
    browserHistory.listen(location => {
      ReactGA.set({ page: location.pathname }); // Update the users current page
      ReactGA.pageview(location.pathname); // Record a pageview for the page.
    });
  }, []);

  return (
      <Grid container spacing={3} alignItems='center' justify='center' style={{ marginTop: "90px" }}>
        <Grid item xs={11}>
          <Typography variant='h4'>Privacy Statement</Typography>
          <Paper className={classes.paper} variant='outlined' >
            <Typography variant='body1' paragraph>This Privacy Statement explains what personal data is collected by the specific Uhrig Lab tool and service you are requesting, for what purposes, how it is processed, and how we keep it secure.</Typography>
            <Typography variant='body1'>The data controller’s contact details are the following and should be used only for data protection queries:</Typography>
            <Typography variant='body1'>R. Glen Uhrig</Typography>
            <Typography variant='body1' display='inline'>Email:{' '}</Typography> 
            <a className={classes.link} href={`mailto:ruhrig@ualberta.ca?subject=DomainViz Privacy Concern`}>
              <Typography variant='body1' display='inline'>ruhrig@ualberta.ca</Typography>
            </a>
            <Typography paragraph/>

            <Typography variant='h5'>Why do we collect your personal data?</Typography>
            <Typography variant='body1' paragraph>Processing your personal data is necessary for our legitimate interest in allowing the day-to-day management, operation and functioning of Uhrig Lab Protein Tools.</Typography>
            
            <Typography variant='h5'>How will your personal data be used?</Typography>
            <Typography variant='body1'>We will use the personal data to:</Typography>
            <Typography variant='body1' display='inline'>1. </Typography>
            <Typography variant='body1' display='inline'>To provide the user access to the service</Typography>
            <Typography/>
            <Typography variant='body1' display='inline'>2. </Typography>
            <Typography variant='body1' display='inline'>To better understand the needs of the users and guide future improvements of the service</Typography>
            <Typography/>
            <Typography variant='body1' display='inline'>3. </Typography>
            <Typography variant='body1' display='inline'>To check that the Terms of Use of the service are followed</Typography>
            <Typography/>
            <Typography variant='body1' display='inline'>4. </Typography>
            <Typography variant='body1' display='inline'>To conduct and monitor data protection activities</Typography>
            <Typography/>
            <Typography variant='body1' display='inline'>5. </Typography>
            <Typography variant='body1' display='inline'>To create anonymous usage statistics</Typography>
            <Typography/>
            <Typography variant='body1' display='inline'>6. </Typography>
            <Typography variant='body1' display='inline'>To conduct and monitor security activities</Typography>
            <Typography paragraph/>
            
            <Typography variant='h5'>Who will have access to your personal data?</Typography>
            <Typography variant='body1'>The personal data will be disclosed to:</Typography>
            <Typography variant='body1' display='inline'>1. </Typography>
            <Typography variant='body1' display='inline'>Authorised University of Alberta staff</Typography>
            <Typography/>
            <Typography variant='body1' display='inline'>2. </Typography>
            <Typography variant='body1' display='inline'>Service providers which Uhrig Lab relies on to provide the service.</Typography>
            <Typography paragraph/>

            <Typography variant='h5'>Will your personal data be transferred to third countries (i.e. countries not part of EU/EAA) and/or international organisations?</Typography>
            <Typography variant='body1'>Personal data is transferred to the following service provider based in a third country which Uhrig Lab relies on to provide the service:</Typography>
            <Typography variant='body1'>Google Analytics</Typography>
            <Typography variant='body1'>Google LLC</Typography>
            <Typography variant='body1'>1600 Amphitheatre Parkway</Typography>
            <Typography variant='body1'>Mountain View, CA 94043</Typography>
            <Typography variant='body1' paragraph>United States</Typography>
            <Typography variant='body1' paragraph>There are no personal data transfers to international organisations.</Typography>

            <Typography variant='h5'>How long do we keep your personal data?</Typography>
            <Typography variant='body1' paragraph>Any personal data directly obtained from you will be retained as long as the service is live, even if you stop using the service. We will keep the personal data for the minimum amount of time possible to ensure legal compliance and to facilitate internal and external audits if they arise.</Typography>
            <Typography variant='body1' paragraph>Google Analytics logs will be kept for 26 months.</Typography>
            <Typography variant='body1' paragraph>User requests will be kept in RT for the duration of the service.</Typography>
            <Typography variant='body1' paragraph>Web logs are kept for 4 weeks.</Typography>

            <Typography variant='h5'>Your rights regarding your personal data</Typography>
            <Typography variant='body1'>You have the right to:</Typography>
            <Typography variant='body1'>1. Not be subject to decisions based solely on an automated processing of data (i.e. without human intervention) without you having your views taken into consideration.</Typography>
            <Typography variant='body1'>2. Request at reasonable intervals and without excessive delay or expense, information about the personal data processed about you. Under your request we will inform you in writing about, for example, the origin of the personal data or the preservation period.</Typography>
            <Typography variant='body1'>3. Request information to understand data processing activities when the results of these activities are applied to you.</Typography>
            <Typography variant='body1'>4. Object at any time to the processing of your personal data unless we can demonstrate that we have legitimate reasons to process your personal data.</Typography>
            <Typography variant='body1' paragraph>5. Request free of charge and without excessive delay rectification or erasure of your personal data.</Typography>

            <Typography variant='body1'>It must be clarified that rights 4 and 5 are only available whenever the processing of your personal data is not necessary to:</Typography>
            <Typography variant='body1'>1. Comply with a legal obligation.</Typography>
            <Typography variant='body1'>2. Perform a task carried out in the public interest.</Typography>
            <Typography variant='body1'>3. Exercise authority as a data controller.</Typography>
            <Typography variant='body1'>4. Archive for purposes in the public interest, or for historical research purposes, or for statistical purposes.</Typography>
            <Typography variant='body1' paragraph>5. Establish, exercise or defend legal claims.</Typography>

            <Typography variant='h5'>Published on:</Typography>
            <Typography variant='body1' paragraph>Wednesday, December 16, 2020</Typography>


          </Paper>
        </Grid>
      </Grid>
  );
}

