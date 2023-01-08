import React, { useState } from 'react'
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack5';

export interface ThesisProps{

}

const Thesis: React.FC<ThesisProps> = ({}) => {
    
    const [numPages, setNumPages] = useState<number | null>(null);
    const [pageNumber, setPageNumber] = useState(1);

    function onDocumentLoadSuccess(numPages: number) {
        setNumPages(numPages);
      }
    return (
    <div style={{width: '100%', border: '1px solid #EEE', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{height: '80vh'}}>
        {/* <Document file={require('./pdfs/Filip_Gacek_Engineering_Thesis.pdf')} onLoadSuccess={onDocumentLoadSuccess}> */}
            {/* <Page pageNumber={1} scale={0.8} /> */}
        {/* </Document> */}
        <p style={{color: '#000'}}>
            Page {pageNumber} of {numPages}
        </p>
        </div>
        
    </div>
  )
}



export default Thesis