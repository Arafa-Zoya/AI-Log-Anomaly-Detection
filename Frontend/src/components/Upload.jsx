import React, { useState, useRef } from 'react';
import { motion } from 'framer-motion';
import { Upload as UploadIcon, FileJson, X } from 'lucide-react';

const Upload = ({ onUpload, loading }) => {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = () => {
    if (file) {
      onUpload(file);
    }
  };

  const clearFile = (e) => {
    e.stopPropagation();
    setFile(null);
  };

  return (
    <motion.div 
      className="glass-card"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      style={{ width: '100%', maxWidth: '600px' }}
    >
      <div 
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current.click()}
      >
        <input 
          ref={inputRef}
          type="file" 
          accept=".csv" 
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        
        {file ? (
          <div style={{ textAlign: 'center' }}>
            <FileJson size={48} className="upload-icon" />
            <div style={{ marginTop: '1rem', fontWeight: 600 }}>{file.name}</div>
            <div style={{ color: '#94a3b8', fontSize: '0.8rem' }}>{(file.size / 1024).toFixed(2)} KB</div>
            <motion.button 
              className="analyze-btn"
              style={{ marginTop: '1.5rem' }}
              onClick={(e) => { e.stopPropagation(); handleSubmit(); }}
              disabled={loading}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              {loading ? <div className="spinner" style={{ width: 20, height: 20 }}></div> : "Initiate Neural Scan"}
            </motion.button>
            <button 
              onClick={clearFile}
              style={{ display: 'block', margin: '1rem auto', background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', fontSize: '0.8rem' }}
            >
              Remove File
            </button>
          </div>
        ) : (
          <>
            <UploadIcon size={48} className="upload-icon" />
            <h3 style={{ margin: '1rem 0 0.5rem' }}>Upload System Logs</h3>
            <p style={{ color: '#94a3b8', textAlign: 'center' }}>
              Drag & Drop your CSV logs here or click to browse.<br/>
              The AI will scan for anomalies in zero gravity.
            </p>
          </>
        )}
      </div>
    </motion.div>
  );
};

export default Upload;
