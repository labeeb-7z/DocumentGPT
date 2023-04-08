import React, { useState } from 'react'
import Qna from './qna'
import PdfViewer from './pdf-viewer'
import Summary from './summary'
import Chatbox from './chatbox'
import { Viewer, Worker, PageLayout } from '@react-pdf-viewer/core';
// Import the styles
import '@react-pdf-viewer/core/lib/styles/index.css';
import UploadPdf from './uploadpdf'
import { useDispatch } from 'react-redux'
//pdf viewer
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';



const pageLayout = {
  transformSize: ({ size }) => ({
    height: size.height + 30,
    width: size.width + 30,
  }),
};


const Main = () => {
  const [selectedText, setSelectedText] = useState("");
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [dragging, setDragging] = useState(false);
  const [isList, setIsList] = useState(false);
  const [isSubList, setIsSubList] = useState(3);
  const dispatch = useDispatch();
  const [question, setquestion] = useState("");
  const [output, setoutput] = useState("");
  const [highlight, sethighlight] = useState(false);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    setFile(e.dataTransfer.files[0]);
    // if (file) {
    //   handleSubmit(e);
    // } else {
    //   alert('Please Upload a File');
    // }
  };

  const handleChange = (e) => {
    e.preventDefault();
    setFile(e.target.files[0]);
    if (file) {
      console.log(file);
      alert('File Uploaded Successfully')
    } else {
      alert('Please Upload a File')
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(file);
    const formData = new FormData();
    formData.append("filetype", "pdf")
    formData.append("file", file);
    formData.append("embed_model", "HF")
    formData.append("llm_model", "Openai")

    setoutput("Proccessing the Document....");
    try {
      const response = await fetch("http://127.0.0.1:8000/process", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      console.log(data);
      setoutput(data);
    } catch (error) {
      console.error(error);
      setoutput("Error Proccessing the pdf");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/queryqna", {
        method: "POST",
        body: question,
      });
      const data = await response.json();
      console.log(data.response);
      setoutput(data.response);
    } catch (error) {
      console.error(error);
      setoutput("Error answering the query");
      return;
    }


  };


  const handleSelection = () => {
    const selection = window.getSelection();
    setSelectedText(selection.toString());
    if (selectedText) {
      handleSubmit();
    }
  };

  const handleAskedQuestion = async () => {
    if (question) {
      const formData = new FormData();
      formData.append("filetype", "pdf")
      formData.append("file", file);
      formData.append("embed_model", "HF")
      formData.append("llm_model", "Openai")

      setoutput("Proccessing the Document....");
      try {
        console.log("hello");
        const response = await fetch("http://192.168.208.155:8000/process", {
          method: "POST",
          body: formData,
        });
        console.log("bye");
        const data = await response.json();
        console.log(data.response);
        setoutput(data.response);
      } catch (error) {
        console.error(error);
        setoutput("Error Proccessing the pdf");
        return;
      }
      const formData2 = new FormData();
      formData2.append("query", question);

      setoutput("Asking AI the question you asked....");

      try {
        const response = await fetch("http://192.168.208.155:8000/queryqna", {
          method: "POST",
          body: formData2,
        });
        const data = await response.json();
        console.log(data.response);
        setoutput(data.response);
      } catch (error) {
        console.error(error);
        setoutput("Error answering the query");
        return;
      }
    } else {
      alert("Ask some question first ...");
    }
  }
  return (
    <div>
      <div className='bg-[#121416]'>
        <div>
          <div className='w-[50rem] mx-auto border p-2 rounded-lg bg-slate-950'>
            <div
              className={`${dragging ? "bg-gray-700" : "bg-slate-950"
                } border-2 border-dashed border-white p-4 rounded-md h-[12rem]`}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <form onSubmit={handleSubmit}>

                <div className="flex flex-col items-center justify-center space-y-2">
                  <img src='/folders.png' className='h-[3rem] w-[3rem] my-5' />
                  <div>
                    <div onClick={() => setIsList(!isList)} className="w-44 p-4 hover:bg-gray-700 rounded border text-sm font-medium leading-none text-white flex items-center justify-between cursor-pointer">
                      CHOOSE FILE
                      <div>
                        {isList ? (
                          <div>
                            <svg width={10} height={6} viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M5.00016 0.666664L9.66683 5.33333L0.333496 5.33333L5.00016 0.666664Z" fill="#FFFFFF" />
                            </svg>
                          </div>
                        ) : (
                          <div>
                            <svg width={10} height={6} viewBox="0 0 10 6" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path d="M5.00016 5.33333L0.333496 0.666664H9.66683L5.00016 5.33333Z" fill="#FFFFFF" />
                            </svg>
                          </div>
                        )}
                      </div>
                    </div>
                    {isList && (
                      <div className="w-44 mt-2 p-2 border border-gray-300 bg-[#121416] shadow rounded">
                        {/* <label> */}
                        {/* <input type="file" className='hidden' /> */}
                        <label htmlFor="file-input">
                          <input
                            id="file-input"
                            type="file"
                            className="hidden"
                            onChange={handleChange}
                          />
                          <div className="text-sm border hover:bg-gray-700 border-gray-300 rounded-md my-1 font-medium py-3 w-full leading-3 pl-9">From Device</div>
                        </label>
                        <button className="text-sm border hover:bg-gray-700 border-gray-300 rounded-md my-1 font-medium py-3 w-full leading-3">From Google Drive</button>
                      </div>
                    )}
                    <style>
                      {` .checkbox:checked + .check-icon {
                display: flex;
            }`}
                    </style>
                  </div>
                </div>
              </form>
              <p className="mt-4">{message}</p>
            </div>
          </div>
        </div >
      </div>
      <div className='bg-[#121416] flex'>
        <div className='w-[50%] pt-20 pl-16 pr-10'>
          <h1 className='p-3 text-2xl'>Selected Document</h1>
          <div className='border p-5 rounded'>
            <div
              style={{
                border: '1px solid rgba(0, 0, 0, 0.3)',
                height: '750px',
              }}
              onMouseUp={handleSelection}
            >
              <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
                <Viewer pageLayout={pageLayout} fileUrl={'/transformers.pdf'} />
              </Worker>
            </div>
          </div>
          <button></button>
        </div>
        <div className="w-[50%] pt-[5rem] pr-20 pl-10">
          <div class="flex items-center mt-14 ml-3">
            <input onChange={(e) => sethighlight(!highlight)} id="default-checkbox" type="checkbox" value="" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600" />
            <label for="default-checkbox" class="ml-2 text-sm font-medium text-white">Ask Question from selected part of document ?</label>
          </div>
          {highlight && (<>
            <h1 className='p-3 text-2xl'>Selected Text</h1>
            <div className="border rounded mb-5">
              <div className="bg-[#121416] m-3">
                <div className="bg-slate-800 p-7 max-h-[10rem] overflow-y-scroll">
                  {selectedText ? selectedText : 'Select Some texts to asks questions to AI.'}
                </div>
              </div>
            </div>
          </>)}
          <h1 className='p-3 text-2xl'>Ask a Question: </h1>
          <div className="mb-3 p-3 flex justify-between">
            <div className='border rounded p-2 w-[82%]'>
              <input placeholder='Ask a question here...' className='bg-slate-800 w-full h-[2.5rem] p-3 ' onChange={(e) => setquestion(e.target.value)} />
            </div>
            <button onClick={handleAskedQuestion} type="button" class="text-white bg-gradient-to-br from-green-400 to-blue-600 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-green-200 dark:focus:ring-green-800 font-medium rounded-lg text-sm px-7 py-2.5 text-center mr-2 mb-2"> Ask</button>
          </div>

          <h1 className='p-3 text-2xl'>AI Output: </h1>
          <div className="border rounded ">
            <Chatbox text={output ? output : "Hello! Ask Me Anything ?"} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Main