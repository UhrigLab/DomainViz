import React from 'react';
import './App.css';
import 'fontsource-roboto';
import { makeStyles } from '@material-ui/core/styles';
import { AppBar, Toolbar, Typography, Button, createMuiTheme, ThemeProvider, Divider, Box, Container } from '@material-ui/core';
import {
  BrowserRouter,
  Switch,
  Route,
  Link,
} from 'react-router-dom';

import { ViewPDF } from './components/ViewPDF';
import Footer from './components/Footer';

import Home from './components/Home';
import { About } from './components/About';
import { Help } from './components/Help';
import { TermsOfUse } from './components/TermsOfUse';
import { PrivacyStatement } from './components/PrivacyStatement';
import DomainViz from './components/DomainViz';
// import MotifX from './components/MotifX';

const useStyles = makeStyles((theme) => ({
  app: {
    minHeight: '85.8vh',
    minWidth: '100%',
    overflow: "hidden",
    display: 'box',
  },
  subtitle: {
    flexGrow: 1,
    fontFamily: `"Raleway"`,
  },
  linkButton: {
    fontFamily: `"Raleway"`,
    fontSize: 20,
    fontStyle: "bold",
    color: "black",
  },
  divider: {
    scale: 1.0,
    backgroundColor: 'black',
  },
  paper: {
    padding: theme.spacing(2),
    textAlign: 'center',
    color: "black",
    backgroundColor: "#e8e8e8"
  },
  appBar: {
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  toolbar: theme.mixins.toolbar,

}));


const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#e8e8e8',
    },
    secondary: {
      // This is green.A700 as hex.
      main: '#000000',
    },
  },
});


function App() {
  const classes = useStyles();
  return (
    <div className="App">
      <BrowserRouter>
      <Container className={classes.app}>
      <ThemeProvider theme={theme}>
        <AppBar postion='fixed' className={classes.appBar}>
          <Toolbar>
            <Box className={classes.paper}>
              <Typography variant='h5' fontWeight='bold' >UHRIG LAB</Typography>
              <Divider className={classes.divider}></Divider>
              <Typography variant='body1' className={classes.subtitle}>Protein tools</Typography>
            </Box>
            <Typography variant="h6" className={classes.subtitle}/> {/* Need this for spacing for now */}
            
            {/* <Link to='/'>
              <Button color='inherit'>Home</Button>
            </Link> */}
            {/* <Link to='/domainviz'> */}
            <Link to='/domainviz'>
              <Button color='inherit' className={classes.linkButton}>DomainViz</Button>
            </Link>
            {/* <Link to='/motif-x'>
              <Button color='inherit'>MotifX</Button>
            </Link> */}
            <Link to='/about'>
              <Button color='inherit' className={classes.linkButton}>About Us</Button>
            </Link>
            <Link to='/help'>
              <Button color='inherit' className={classes.linkButton}>Help</Button>
            </Link>
            <Button target="_blank" color='inherit' href="https://www.uhriglab.com/" className={classes.linkButton}>Lab Website</Button>

          </Toolbar>
        </AppBar>

        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/about" component={About} />
          <Route path="/view-results/" component={ViewPDF} />
          <Route path="/domainviz" component={DomainViz} />
          <Route path="/help" component={Help} />
          <Route path='/terms-of-use' component={TermsOfUse}/>
          <Route path='/privacy-statement' component={PrivacyStatement}/>

          {/* <Route path="/motif-x" component={MotifX} /> */}
        </Switch>

      </ThemeProvider>
      </Container>
      <Footer></Footer>
      </BrowserRouter>


    </div>

  );
}

export default App;
