import React, { useState } from 'react'
// child
import { Viewer, Worker, PageLayout } from '@react-pdf-viewer/core';
// Import the styles
import '@react-pdf-viewer/core/lib/styles/index.css';
import { useDispatch } from 'react-redux';


const pageLayout = {
    transformSize: ({ size }) => ({
        height: size.height + 30,
        width: size.width + 30,
    }),
};

const UploadPdf = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [dragging, setDragging] = useState(false);
    const [isList, setIsList] = useState(false);
    const [isSubList, setIsSubList] = useState(3);
    const dispatch = useDispatch();

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
        if (file) {
            handleSubmit(e);
        } else {
            alert('Please Upload a File');
        }
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
        dispatch({
            type: 'SET_DATA',
            payload: file,
        });
        // const formData = new FormData();
        // formData.append("file", file);
        
        // try {
        //     const response = await fetch("http://127.0.0.1:8000/upload", {
        //         method: "POST",
        //         body: formData,
        //     });
        //     const data = await response.json();
        //     console.log(data);
        // } catch (error) {
        //     console.error(error);
        // }
    };
    return (
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
    )
}

export default UploadPdf;