import React, { useEffect, useState } from 'react';
import './App.css';
import { Images } from './Images';

function App() {

  const [images, setImages] = useState([]);

  useEffect(() => {
    fetch('/images').then(response => 
      response.json().then(data => {
        setImages(data.images)
      })
    );
  },[]);

  return (
    <div className="App">
      <Images images={images}/>
    </div>
  );
}

export default App;
