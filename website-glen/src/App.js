import React from 'react';
import './App.css';
import 'fontsource-roboto';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import MenuIcon from '@material-ui/icons/Menu';
import { makeStyles } from '@material-ui/core/styles';
import { AppBar, IconButton, Toolbar, Typography, Button } from '@material-ui/core';
import {
  BrowserRouter,
  Switch,
  Route,
  Link,
} from 'react-router-dom';

import { ViewPDF } from './components/ViewPDF';
import Home from './components/Home';
import About from './components/About';
import ProtPlot from './components/ProtPlot';
import MotifX from './components/MotifX';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

function App() {
  const classes = useStyles();
  return (
    <div className="App">
      <BrowserRouter>
        <AppBar postion='static'>
          <Toolbar>
            <IconButton edge="start" className={classes.menuButton} color="inherit" aria-label="menu">
              <MenuIcon />
            </IconButton>
            <Typography variant="h6" className={classes.title}>
              Uhrig Lab
            </Typography>
            <Link to='/'>
              <Button color='inherit'>Home</Button>
            </Link>
            <Link to='/protplot'>
              <Button color='inherit'>ProDoPlot</Button>
            </Link>
            {/* <Link to='/motif-x'>
              <Button color='inherit'>MotifX</Button>
            </Link> */}
            <Link to='/about'>
              <Button color='inherit'>About Us</Button>
            </Link>

          </Toolbar>
        </AppBar>

        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/about" component={About} />
          <Route path="/view-results/" component={ViewPDF} />
          <Route path="/protplot" component={ProtPlot} />
          <Route path="/motif-x" component={MotifX} />
        </Switch>
      </BrowserRouter>

    </div>

  );
}

export default App;
