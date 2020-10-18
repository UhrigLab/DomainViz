import React, { useRef} from 'react';
import {ReactComponent as UploadIcon} from './icons/upload-file.svg' 



function UploadFile({ handleFile }) {
    // Create a reference to the hidden file input element
    const hiddenInput = useRef(null);

    // onClick function for the "Upload" button
    function uploadButtonClick() {
        hiddenInput.current.click();
    }

    const handleChange = e => {
        const fileUploaded = e.target.files[0];
        handleFile(fileUploaded);
    }
  return (
    <div>
        <UploadIcon onClick={uploadButtonClick}/>        
        <input type="file" ref={hiddenInput} onChange={handleChange} style={{display: 'none'}}/>    </div>
  );
}

export default UploadFile;
