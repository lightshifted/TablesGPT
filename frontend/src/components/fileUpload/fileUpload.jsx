import React, { useState } from 'react';
import './fileUpload.css';
import DictTable from '../dictTable/dictTable';

const FileUpload = () => {
  const [dragging, setDragging] = useState(false);
  const [file, setFile] = useState(null);
  const [showDictTable, setShowDictTable] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const file = e.dataTransfer.files[0];
    setFile(file)
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setShowDictTable(true);
        setErrorMessage(null); // Reset the error message
        setIsLoading(false);
      })
      .catch((error) => {
        console.error(error);
        setErrorMessage(error.message);
        setIsLoading(false);
      });
  };

  return (
    <div display="flex">
    {!showDictTable && (
    <div
      className={`file-upload-container${dragging ? ' dragging' : ''}`}
      onDragEnter={handleDragEnter}
      onDragOver={handleDragEnter}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
    
      <div className="file-upload-message">
        {file ? (
          <>
            <p className="file-name">{file.name}</p>
            <button className="submit-button" onClick={handleSubmit}>Generate Table</button>
            {isLoading && <p className="loading-message">Loading table data...</p>}
            {errorMessage && <p className="error-message">{errorMessage}</p>}
          </>
        ) : (
          <>
            <p className="drag-drop-message">Drag and drop your file here</p>
            <p className="or-message">or</p>
            <label htmlFor="file-input" className="browse-link">
              Browse
            </label>
            <input
              type="file"
              id="file-input"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ display: 'none' }}
            />
          </>
        )}
      </div>
    </div>
    )}
    <div>
      {showDictTable && <DictTable file={file}/>}
    </div>
    </div>
  );
};

export default FileUpload;
