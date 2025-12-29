import React, { useState } from 'react';
import uploadService from '../../services/uploadService';
import { toast } from 'react-toastify';
import './FileUpload.css';

const FileUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [layerName, setLayerName] = useState('');
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (selectedFile) => {
    setFile(selectedFile);
    // Auto-generate layer name from filename
    const name = selectedFile.name
      .replace(/\.(zip|geojson|json)$/i, '')
      .replace(/[^a-z0-9_]/gi, '_')
      .toLowerCase();
    setLayerName(name);
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file || !layerName) {
      toast.error('Please select a file and enter a layer name');
      return;
    }

    setUploading(true);
    setProgress(0);

    try {
      let result;
      if (file.name.endsWith('.zip')) {
        result = await uploadService.uploadShapefile(file, layerName, setProgress);
      } else if (file.name.endsWith('.geojson') || file.name.endsWith('.json')) {
        result = await uploadService.uploadGeoJSON(file, layerName, setProgress);
      } else {
        toast.error('Invalid file type. Please upload a ZIP (shapefile) or GeoJSON file.');
        setUploading(false);
        return;
      }

      if (result.success) {
        toast.success(result.message);
        setFile(null);
        setLayerName('');
        setProgress(0);
        if (onUploadSuccess) {
          onUploadSuccess(result);
        }
      } else {
        toast.error(result.message || 'Upload failed');
      }
    } catch (error) {
      toast.error('Upload error: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload">
      <h3>Upload Data</h3>
      <div
        className={`drop-zone ${dragActive ? 'active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-input"
          accept=".zip,.geojson,.json"
          onChange={handleFileChange}
          disabled={uploading}
        />
        <label htmlFor="file-input">
          {file ? (
            <div>
              <strong>Selected file:</strong> {file.name}
            </div>
          ) : (
            <div>
              <p>Drag & drop file here or click to browse</p>
              <p className="file-types">Supported: Shapefile (.zip), GeoJSON (.geojson, .json)</p>
            </div>
          )}
        </label>
      </div>

      {file && (
        <div className="upload-form">
          <div className="form-group">
            <label htmlFor="layer-name">Layer Name:</label>
            <input
              type="text"
              id="layer-name"
              value={layerName}
              onChange={(e) => setLayerName(e.target.value)}
              placeholder="Enter layer name"
              disabled={uploading}
            />
          </div>

          {uploading && (
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}>
                {progress}%
              </div>
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={uploading || !file || !layerName}
            className="btn-upload"
          >
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
