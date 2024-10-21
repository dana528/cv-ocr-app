import React, { useState } from 'react';
import { MdCloudUpload, MdDelete } from 'react-icons/md';
import { AiFillFileImage } from 'react-icons/ai';

function Uploader({ onUpload, docType }) { // Accept onUpload and docType as props

    const [image, setImage] = useState(null);
    const [fileName, setFileName] = useState('No selected File');
    const [dragActive, setDragActive] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        setDragActive(true);
    };

    const handleDragLeave = () => {
        setDragActive(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setDragActive(false);
        const files = e.dataTransfer.files;
        if (files && files[0]) {
            setFileName(files[0].name);
            setImage(URL.createObjectURL(files[0]));
            setSelectedFile(files[0]);
        }
    };

    const handleFileChange = ({ target: { files } }) => {
        if (files && files[0]) {
            setFileName(files[0].name);
            setImage(URL.createObjectURL(files[0]));
            setSelectedFile(files[0]);
        }
    };

    const handleUpload = async () => {
        if (selectedFile) {
            const extractedInfo = await onUpload(selectedFile, docType); // Call onUpload and pass docType
            return extractedInfo;
        }
    };

    return (
        <div className="p-4 w-full max-w-lg bg-white shadow-lg rounded-lg">
          <div className="flex items-center pb-3 border-b border-gray-200">
            <div className="flex-1">
              <h3 className="text-gray-800 text-xl font-bold">Upload File</h3>
            </div>
          </div>
    
          {/* Drag and Drop or File Selection */}
          <div
            className={`rounded-lg border-2 border-gray-200 border-dashed mt-6 ${dragActive ? 'bg-gray-100' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.querySelector('#chooseFile').click()}
          >
            <div className="p-4 min-h-[180px] flex flex-col items-center justify-center text-center cursor-pointer">
              {image ? (
                <img src={image} width={60} height={60} alt={fileName} />
              ) : (
                <>
                  <AiFillFileImage className="w-10 mb-4 fill-gray-600 inline-block" />
                  <h4 className="text-sm text-gray-600">Drag & Drop or <label htmlFor="chooseFile" className="text-blue-600 cursor-pointer">Choose file</label> to upload</h4>
                  <input type="file" id="chooseFile" accept="image/*" className="hidden" onChange={handleFileChange} />
                </>
              )}
            </div>
          </div>
    
          {/* File Details */}
          <div className="flex flex-col bg-gray-50 p-4 rounded-lg mt-4">
            <div className="flex items-center">
              <AiFillFileImage color='#1475cf' />
              <span className="ml-4 flex-1 text-xs text-gray-600">
                {fileName !== 'No selected File' && selectedFile ? (
                  <>{fileName} <MdDelete onClick={() => {
                    setFileName("No selected File");
                    setImage(null);
                    setSelectedFile(null);
                  }} />
                  </>
                ) : (
                  "No file selected"
                )}
              </span>
            </div>
          </div>
    
          {/* Upload Progress or Buttons */}
          <div className="border-t border-gray-200 pt-6 flex justify-between gap-4 mt-6">
            <button
              type="button"
              className="w-full px-4 py-2 rounded-lg text-gray-800 text-sm bg-gray-200 hover:bg-gray-300"
              onClick={() => {
                setFileName("No selected File");
                setImage(null);
                setSelectedFile(null);
              }}
            >
              Cancel
            </button>
            <button
              type="button"
              className="w-full px-4 py-2 rounded-lg text-white text-sm bg-blue-600 hover:bg-blue-700"
              onClick={handleUpload}
              disabled={!selectedFile}
            >
              Upload
            </button>
          </div>
        </div>
      );
    }
    
    export default Uploader;