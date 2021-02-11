import { saveAs } from 'file-saver';


export function downloadTestFastaFile() {
    fetch('/api/testFasta').then(response => {
        saveAs(response.url);
    });
}

