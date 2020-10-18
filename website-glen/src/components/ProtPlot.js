import React, { useRef } from 'react';
import UploadFile from './UploadFile';



function ProtPlot() {

    function handleFastaFile(file) {
        const fastaFile = file;
        console.log(fastaFile.name);
    }

    return (
        <div>
            <h3>Protplot page</h3>
            <p>Instructions: Use this program ... FILL ME IN ... </p>
            <div>
                <p>Fasta File:</p>
                <UploadFile handleFile={handleFastaFile}></UploadFile>
            </div>
        </div>
  );
}

export default ProtPlot;
