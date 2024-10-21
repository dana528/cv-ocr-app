import React, { useState } from 'react';
import Tabs from './Tabs/Tabs';
import Uploader from './Uploader/Uploader';
import DLInfo from './ExtractedInfo/DLInfo';
import PassportInfo from './ExtractedInfo/PassportInfo';
import CRBookInfo from './ExtractedInfo/CRBookInfo';

const DocumentExtractor = () => {
  const [activeTab, setActiveTab] = useState('dl'); 
  const [results, setResults] = useState(null); 
  const handleUpload = async (file, docType) => {
    if (!file) {
      alert('Please select an image to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('image', file);
    formData.append('doc_type', activeTab === 'dl' ? 'DL' : activeTab === 'passport' ? 'Passport' : 'CRBook');

    try {
      const response = await fetch('http://localhost:8000/process', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResults(data.extracted_info);
      return data.extracted_info;
    } catch (error) {
      console.error('Error:', error);
      alert('Error processing image.');
      return null;
    }
  };

  return (
    <div class='flex flex-col items-center font-sans'>
      <h1 class='text-3xl mb-5 font-semibold text-slate-950'>
        Document Info Extractor Application
      </h1>

      <Tabs 
      class='align-center'
      activeTab={activeTab} 
      setActiveTab={setActiveTab} 
      />

      <div className="flex flex-row w-full max-w-6xl mt-10  gap-4">
        <div className="flex-1 mr-50">
          <Uploader
            onUpload={handleUpload} 
            docType={activeTab === 'dl' ? 'DL' : activeTab === 'passport' ? 'Passport' : 'CRBook'} // Pass the document type
          />
        </div>

        <div className="flex-1 ml-30 bg-white shadow-lg rounded-lg p-6">
          {results ? (
            <>
              {activeTab === 'dl' && <DLInfo details={results} />}
              {activeTab === 'passport' && <PassportInfo details={results} />}
              {activeTab === 'crbook' && <CRBookInfo details={results} />}
            </>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-gray-500 text-center">
                No uploaded image.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DocumentExtractor;
