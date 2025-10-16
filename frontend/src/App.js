import './App.css';
import { useState, useRef } from 'react';
import { uploadFile } from './utils/processFile'

export default function App() {
  const [newFile, setNewFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const inputFile = useRef(null)


  const getFileData = async(f) => {

    try{
    
      let fileData = await uploadFile(f);
      console.log("Duration of video: ", fileData); 

    } catch (error) {
      console.log("No Duration received", error);
    }
  }

  const openBrowse = () => {
    inputFile.current.click();
    console.log("Opening Browser");
  }

  
  const handleFileSelect = async(e) => {
    try{  
      const f = e.target.files[0]
      setNewFile(f);
      console.log("Got File!");

      await getFileData(f)

      if (inputFile.current) inputFile.current.value = '';

    } catch(error) {
      console.log("File Upload Error:", error);
    }
  }

  function handleDragOver(e){
    e.preventDefault(); //prevents browswers default handling of files
    //such as file opening (new tabs and such)
   
  }

  const handleDrop = async(e) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    setNewFile(f);
    await getFileData(f);
    setIsDragOver(false);
    console.log("Got File!");
  }

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };
  
  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragOver(false);
  };
  

  return (
    <div className="App">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="main-title">SCLIP</h1>
          <p className="subtitle">How Skilled Are You?</p>
          <div className="upload-container">
            <div className={`upload-box ${ isDragOver ? 'drag-over' : '' }`}
              onClick={openBrowse}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <input onChange={handleFileSelect} type='file' id='file' ref={inputFile} style={{display: 'none'}}/> 
              <div className="upload-icon">📁</div>
              <p className="upload-text">Drop your video here or click to browse</p>
              <p className="upload-hint">Supports MP4, AVI, MOV files</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


