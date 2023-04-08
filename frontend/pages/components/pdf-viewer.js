import React, { useState } from 'react'
import { Viewer, Worker, PageLayout } from '@react-pdf-viewer/core';
// Import the styles
import '@react-pdf-viewer/core/lib/styles/index.css';


const pageLayout = {
    transformSize: ({ size }) => ({
        height: size.height + 30,
        width: size.width + 30,
    }),
};




const PdfViewer = () => {

    const [selectedText, setSelectedText] = useState("");

    const handleSelection = () => {
        const selection = window.getSelection();
        setSelectedText(selection.toString());
    };
    console.log(selectedText);
    return (
        <div
            style={{
                border: '1px solid rgba(0, 0, 0, 0.3)',
                height: '750px',
            }}
            onMouseUp={handleSelection}
        >
            <Worker  workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
                <Viewer pageLayout={pageLayout} fileUrl="/try.pdf" />
            </Worker>
        </div>
    )
}

export default PdfViewer