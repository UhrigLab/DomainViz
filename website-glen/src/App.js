import React from 'react';
import './App.css';
import 'fontsource-roboto';
import ArrowDropDownIcon from '@material-ui/icons/ArrowDropDown';
import {
  BrowserRouter,
  Switch,
  Route,
} from 'react-router-dom';

import { ViewPDF } from './components/ViewPDF';
import DropdownMenu from './components/DropdownMenu';
import Navbar from './components/Navbar';
import NavItem from './components/NavItem';
import Home from './components/Home';
import About from './components/About';
import ProtPlot from './components/ProtPlot';
import MotifX from './components/MotifX';

function App() {
  
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar>
          <NavItem icon={<ArrowDropDownIcon/>}>
            <DropdownMenu></DropdownMenu>
          </NavItem>
        </Navbar>

        <Switch>
          <Route path="/" exact component={Home}/>
          <Route path="/about" component={About}/>
          <Route path="/view-results/" component={ViewPDF}/> 
          <Route path="/protplot" component={ProtPlot}/>
          <Route path="/motif-x" component={MotifX}/>
        </Switch>
      </BrowserRouter>
     
    </div>
    
  );
}

export default App;
