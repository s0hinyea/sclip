import './App.css';

function App() {
  return (
    <div className="App">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="main-title">SCLIP</h1>
          <p className="subtitle">How Skilled Are You?</p>
          <div className="upload-container">
            <div className="upload-box">
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

export default App;
