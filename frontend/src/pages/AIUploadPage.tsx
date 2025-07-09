import React, { useState, useRef, useContext } from "react";
import { Link } from "react-router-dom";
import AuthContext from "../components/context/AuthContext";
import { uploadFilesForAI } from "../api/apiRequests";
import "../css/AIUploadPage.css";

interface UploadedFile {
  file: File;
  id: string;
  preview?: string;
}

const AIUploadPage = () => {
  const authData = useContext(AuthContext);
  const [dragActive, setDragActive] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const allowedTypes = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "application/pdf",
    "image/webp",
  ];
  const maxFileSize = 10 * 1024 * 1024; // 10MB

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    handleFiles(files);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      const files = Array.from(e.target.files);
      handleFiles(files);
    }
  };

  const handleFiles = (files: File[]) => {
    files.forEach((file) => {
      if (!allowedTypes.includes(file.type)) {
        alert(
          `File type ${file.type} is not supported. Please upload images (JPEG, PNG, GIF, WebP) or PDF files.`
        );
        return;
      }

      if (file.size > maxFileSize) {
        alert(`File ${file.name} is too large. Maximum size is 10MB.`);
        return;
      }

      const id =
        Date.now().toString() + Math.random().toString(36).substr(2, 9);
      const newFile: UploadedFile = { file, id };

      // Create preview for images
      if (file.type.startsWith("image/")) {
        const reader = new FileReader();
        reader.onload = (e) => {
          setUploadedFiles((prev) =>
            prev.map((f) =>
              f.id === id ? { ...f, preview: e.target?.result as string } : f
            )
          );
        };
        reader.readAsDataURL(file);
      }

      setUploadedFiles((prev) => [...prev, newFile]);
    });
  };

  const removeFile = (id: string) => {
    setUploadedFiles((prev) => prev.filter((file) => file.id !== id));
  };

  const handleUpload = async () => {
    if (uploadedFiles.length === 0) {
      alert("Please select files to upload.");
      return;
    }

    setIsUploading(true);

    try {
      const formData = new FormData();
      uploadedFiles.forEach((fileData, index) => {
        formData.append(`files`, fileData.file);
      });

      const result = await uploadFilesForAI(authData.access_token, formData);
      console.log("Upload successful:", result);

      // TODO: Handle successful upload (redirect to generated course, show success message, etc.)
      alert(
        "Files uploaded successfully! AI is processing your training materials and will generate a course shortly."
      );

      // Clear uploaded files after successful upload
      setUploadedFiles([]);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const onButtonClick = () => {
    inputRef.current?.click();
  };

  return (
    <div className="basic-page">
      <div style={{ position: "relative" }}>
        <div
          className="assets__background__gradient"
          style={{ top: "0", left: "0" }}
        ></div>
      </div>

      <Link to="/upload-training" className="back-link">
        <span className="back-arrow">←</span> Back to Creator
      </Link>
      <div className="ai-upload-container">
        <div className="ai-upload-header">
          <div className="ai-upload-title">
            <span className="ai-title-icon">🤖</span>
            AI Course Generator
          </div>
          <p className="ai-upload-subtitle">
            Upload your training materials and let AI create a personalized
            course for you
          </p>
        </div>

        <div className="upload-section">
          <div
            className={`drop-zone ${dragActive ? "drag-active" : ""}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={onButtonClick}
          >
            <input
              ref={inputRef}
              type="file"
              multiple
              onChange={handleChange}
              accept=".jpg,.jpeg,.png,.gif,.pdf,.webp"
              style={{ display: "none" }}
            />

            <div className="drop-zone-content">
              <div className="upload-icon">📁</div>
              <h3>Drag & Drop your files here</h3>
              <p>or click to browse files</p>
              <div className="supported-formats">
                <span>Supported formats: JPEG, PNG, GIF, WebP, PDF</span>
                <span>Maximum size: 10MB per file</span>
              </div>
            </div>
          </div>

          {uploadedFiles.length > 0 && (
            <div className="uploaded-files">
              <h4>Uploaded Files ({uploadedFiles.length})</h4>
              <div className="files-grid">
                {uploadedFiles.map((fileData) => (
                  <div key={fileData.id} className="file-item">
                    <div className="file-preview">
                      {fileData.preview ? (
                        <img src={fileData.preview} alt={fileData.file.name} />
                      ) : (
                        <div className="file-icon">
                          {fileData.file.type === "application/pdf"
                            ? "📄"
                            : "📎"}
                        </div>
                      )}
                    </div>
                    <div className="file-info">
                      <span className="file-name" title={fileData.file.name}>
                        {fileData.file.name.length > 20
                          ? fileData.file.name.substring(0, 20) + "..."
                          : fileData.file.name}
                      </span>
                      <span className="file-size">
                        {(fileData.file.size / 1024 / 1024).toFixed(2)} MB
                      </span>
                    </div>
                    <button
                      className="remove-file"
                      onClick={() => removeFile(fileData.id)}
                      title="Remove file"
                    >
                      ✕
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="upload-actions">
            <button
              className="btn-ai-upload"
              onClick={handleUpload}
              disabled={isUploading || uploadedFiles.length === 0}
            >
              {isUploading ? (
                <>
                  <span className="loading-spinner">⏳</span>
                  Processing...
                </>
              ) : (
                <>
                  <span className="ai-icon">🚀</span>
                  Generate Course with AI
                  <span className="ai-sparkle">✨</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AIUploadPage;
