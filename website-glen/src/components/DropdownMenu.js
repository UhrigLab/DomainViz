import React, { useState, useEffect, useRef } from 'react';

import { ReactComponent as HomeIcon } from './icons/home.svg';
import { ReactComponent as WrenchIcon } from './icons/open-wrench-tool-silhouette.svg';
import { ReactComponent as HelpIcon } from './icons/question-mark-on-a-circular-black-background.svg';
import { Link } from 'react-router-dom';


import { CSSTransition } from 'react-transition-group';

function DropdownMenu() {
  const [activeMenu, setActiveMenu] = useState('main');
  const [menuHeight, setMenuHeight] = useState(null);
  const dropdownRef = useRef(null);

  useEffect(() => {
    setMenuHeight(dropdownRef.current?.firstChild.offsetHeight)
  }, []);

  function calcHeight(el) {
    const height = el.offsetHeight;
    setMenuHeight(height);
  }

  /* A DropdownItem is a component that is nested inside the DropdownMenu. To use, add them inbetween the CSSTransition below. */
  function DropdownItem(props) {
    return (
      <a href='#' className='menu-item' onClick={() => props.goToMenu && setActiveMenu(props.goToMenu)}>
        <span className="icon-button">{props.leftIcon}</span>
        { props.children}
        <span className="icon-right">{props.rightIcon}</span>
      </a>
    );
  }

  return (
    <div className="dropdown" style={{ height: menuHeight }}>

      <CSSTransition
        in={activeMenu === 'main'} // {/* activeMenu means what menu we are currently on, default is 'main' */} 
        unmountOnExit
        timeout={500}
        classNames="menu-primary"
        onEnter={calcHeight}>
        <div className='menu'>
          {/* DropdownItems go inside this div tag */}

          <Link to='/'>
            <DropdownItem
              leftIcon={<HomeIcon />}>
              Home
            </DropdownItem>
          </Link>

          <Link to='/protplot'>
            <DropdownItem
              leftIcon={<WrenchIcon />}>
              PropPlot
            </DropdownItem>
          </Link>

          <Link to='/motif-x'>
            <DropdownItem
              leftIcon={<WrenchIcon />}>
              Motif-x
              </DropdownItem>
          </Link>

          <Link to='/about'>
            <DropdownItem
              leftIcon={<HelpIcon />}>
              About Us
              </DropdownItem>
          </Link>

        </div>
      </CSSTransition>
    </div>
  );
}
export default DropdownMenu;