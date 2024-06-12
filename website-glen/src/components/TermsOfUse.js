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
}));

const browserHistory = createBrowserHistory();
export const TermsOfUse = () => {
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
          <Typography variant='h4'>Terms of use</Typography>
          <Paper className={classes.paper} variant='outlined' >
            <Typography variant='h5'>General</Typography>
            <Typography variant='body1'>1. The Uhrig Lab promotes open science through making scientific data openly and freely accessible.</Typography>
            <Typography variant='body1'>2. We expect attribution (e.g. in publications, services or products) for any and all of our software tools, online services and results thereof in accordance with good scientific practice. The expected attribution will be indicated on the appropriate web page.</Typography>
            <Typography variant='body1'>3. Any feedback provided to the Uhrig Lab regarding our tools  will be treated as non-confidential unless the individual or organisation providing the feedback states otherwise.</Typography>
            <Typography variant='body1'>4. The Uhrig Lab is not liable to you or third parties claiming through you, for any loss or damage.</Typography>
            <Typography variant='body1'>5. Any personal data held by the Uhrig Lab will only be released in exceptional circumstances when required by law or judicial or regulatory order. The Uhrig Lab may make information about the total volume of usage of particular software or data available to the public and third party organisations without details of any individual’s use.</Typography>
            <Typography variant='body1'>6. While we will retain our commitment to OpenScience, we reserve the right to update these Terms of Use at any time. When alterations are inevitable, we will attempt to give reasonable notice of any changes by placing a notice on our website, but you may wish to check each time you use the website. The date of the most recent revision will appear on this, the page. If you do not agree to these changes, please do not continue to use our online services. </Typography>
            <Typography variant='body1' paragraph>7. Any questions or comments concerning these Terms of Use can be addressed to: Dr. R. Glen Uhrig, Department of Biological Sciences, University of Alberta, Edmonton, Alberta, Canada T6G 2E9.</Typography>

            <Typography variant='h5'>Online Services</Typography>
            <Typography variant='body1'>1. Users of  Uhrig Lab online services agree not to attempt to use any Uhrig Lab computers, files or networks apart from through the service interfaces provided.</Typography>
            <Typography variant='body1'>2. The Uhrig Lab will make all reasonable effort to maintain continuity of these online services and provide adequate warning of any changes or discontinuities. However, we  accept no responsibility for the consequences of any temporary or permanent discontinuity in service.</Typography>
            <Typography variant='body1'>3. Any attempt to use Uhrig Lab online services to a level that prevents, or looks likely to prevent, us providing services to others, will result in the use being blocked. We will attempt to contact the user to discuss their needs and how (and if) these can be met from other sources.</Typography>
            <Typography variant='body1'>4. You may not post or send offensive, inappropriate or objectionable content anywhere on or to our websites or otherwise engage in any disruptive behaviour on any of our services. Where we reasonably believe that you are or may be in breach of any applicable laws we may use any available personal information to inform relevant third parties about the content and your behaviour.</Typography>
            <Typography variant='body1'>5. Software that can be run from the Uhrig Lab webpages may be used by any individual for any purpose unless specific exceptions are stated on the web page. Any software made available for download through our web pages will have its own individual license agreement.</Typography>
            <Typography variant='body1' paragraph>6. The Uhrig Lab does not accept responsibility for the consequences of any breach of the confidentiality of the Uhrig Lab Protein Tools site by third parties.</Typography>

            <Typography variant='h5'>Data Services</Typography>
            <Typography variant='body1'>1. The online data services and databases used here are generated in part from data contributed by the community who remain the data owners.</Typography>
            <Typography variant='body1'>2. When you contribute scientific data to a database through our website or other submission tools this information will be released at a time and in a manner consistent with the scientific data and we may store it permanently.</Typography>
            <Typography variant='body1'>3. The Uhrig Lab itself places no additional restrictions on the use or redistribution of the data available via its online services other than those provided by the original data owners.</Typography>
            <Typography variant='body1'>4. The Uhrig Lab does not guarantee the accuracy of any provided data, generated database, software or online service nor the suitability of databases, software and online services for any purpose.</Typography>
            <Typography variant='body1' paragraph>5. The original data may be subject to rights claimed by third parties, including but not limited to, patent, copyright, other intellectual property rights, biodiversity-related access and benefit-sharing rights. It is the responsibility of users of our services to ensure that their exploitation of the data does not infringe any of the rights of such third parties.</Typography>

            <Typography variant='body1'>The Terms of Use and the use of the Uhrig Lab Protein Tools website are governed by Canadian law. </Typography>

          </Paper>
        </Grid>
      </Grid>
  );
}

