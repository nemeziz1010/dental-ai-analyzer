// App.jsx

import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown'; // Import the new library

// --- Helper Components ---

// Simple loading spinner component
const Spinner = () => (
  <div className="flex justify-center items-center">
    <div className="w-8 h-8 border-4 border-cyan-500 border-t-transparent border-solid rounded-full animate-spin"></div>
  </div>
);

// Component for the styled file input button
const FileInput = ({ onFileSelect, disabled }) => {
  const fileInputRef = useRef(null);
  const handleButtonClick = () => fileInputRef.current.click();
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) onFileSelect(file);
  };

  return (
    <>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
        accept=".dcm,.dicom,.rvg"
        disabled={disabled}
      />
      <button
        onClick={handleButtonClick}
        disabled={disabled}
        className="w-full bg-gray-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-gray-700 disabled:bg-gray-500 disabled:cursor-not-allowed transition-colors duration-300 shadow-md"
      >
        Select DICOM File
      </button>
    </>
  );
};

// Main App Component
const App = () => {
  // --- State Management ---
  const [selectedFile, setSelectedFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [fileName, setFileName] = useState('');

  // Ref to access the canvas and its container
  const canvasRef = useRef(null);
  const canvasContainerRef = useRef(null);


  // --- Effect to draw on the canvas responsively ---
  useEffect(() => {
    if (!analysisResult) return;

    const canvas = canvasRef.current;
    const container = canvasContainerRef.current;
    const context = canvas.getContext('2d');
    const image = new Image();

    image.src = `data:image/png;base64,${analysisResult.image_b64}`;

    image.onload = () => {
      // Calculate the aspect ratio to fit the image in the container
      const containerWidth = container.clientWidth;
      const scale = containerWidth / image.width;
      const canvasWidth = containerWidth;
      const canvasHeight = image.height * scale;

      // Set canvas dimensions
      canvas.width = canvasWidth;
      canvas.height = canvasHeight;

      // Clear previous drawings and draw the scaled image
      context.clearRect(0, 0, canvas.width, canvas.height);
      context.drawImage(image, 0, 0, canvas.width, canvas.height);

      // Draw scaled annotations
      analysisResult.annotations.forEach(ann => {
        // Roboflow gives center x, y. Convert to top-left.
        const originalX = ann.x - ann.width / 2;
        const originalY = ann.y - ann.height / 2;

        // Scale all annotation coordinates and dimensions
        const x = originalX * scale;
        const y = originalY * scale;
        const width = ann.width * scale;
        const height = ann.height * scale;
        
        // Draw bounding box
        context.strokeStyle = '#22d3ee'; // A bright cyan color
        context.lineWidth = Math.max(2, 2 * scale); // Scale line width too
        context.strokeRect(x, y, width, height);
        
        // Prepare label
        const label = `${ann.class_name} (${(ann.confidence * 100).toFixed(0)}%)`;
        const fontSize = Math.max(12, 14 * scale);
        context.font = `bold ${fontSize}px sans-serif`;
        const textWidth = context.measureText(label).width;
        const textHeight = fontSize * 1.2;

        // Draw label background
        context.fillStyle = '#22d3ee';
        context.fillRect(x, y - textHeight, textWidth + 10, textHeight);
        
        // Draw label text
        context.fillStyle = '#000000';
        context.fillText(label, x + 5, y - (textHeight / 10));
      });
    };

    image.onerror = () => setError("Failed to load the analysis image.");

  }, [analysisResult]); // Rerun when result is available


  // --- Event Handlers ---
  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setFileName(file.name);
    setAnalysisResult(null);
    setError('');
    const canvas = canvasRef.current;
    if(canvas){
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
        canvas.width=0; // Reset canvas size
        canvas.height=0;
    }
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setError('Please select a file first.');
      return;
    }
    setIsLoading(true);
    setError('');
    setAnalysisResult(null);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://127.0.0.1:8000/analysis/analyze', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setAnalysisResult(data);
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  // --- Render ---
  return (
    <div className="bg-gray-900 text-gray-100 max-h-screen w-screen overflow-hidden font-sans">
      <div className="container mx-auto p-4 sm:p-6 md:p-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-cyan-400">Dental AI Analyzer</h1>
          <p className="text-gray-400 mt-2">Upload a DICOM X-ray to detect pathologies with AI.</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-5 gap-8">
          {/* Left Panel */}
          <div className="lg:col-span-3 bg-gray-800 p-8 rounded-xl shadow-2xl flex flex-col">
            <div className="controls mb-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                 <FileInput onFileSelect={handleFileSelect} disabled={isLoading} />
                 <button
                    onClick={handleAnalyze}
                    disabled={!selectedFile || isLoading}
                    className="w-full bg-cyan-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-cyan-700 disabled:bg-cyan-800/50 disabled:text-gray-400 disabled:cursor-not-allowed transition-all duration-300 shadow-lg"
                  >
                    {isLoading ? 'Analyzing...' : 'Analyze Image'}
                  </button>
              </div>
              {fileName && <p className="text-center text-sm text-gray-400 mt-3 truncate px-4">Selected: {fileName}</p>}
            </div>
            
            <div ref={canvasContainerRef} className="image-viewer  bg-black/50 rounded-lg  min-h-[400px] md:min-h-[500px] w-full h-full">
                {isLoading && <Spinner />}
                <canvas ref={canvasRef} />
                {!isLoading && !analysisResult && !error && (
                    <div className="text-center text-gray-500 my-auto">
                        <p>Image will be displayed here after analysis</p>
                    </div>
                )}
            </div>
          </div>

          {/* Right Panel */}
          <div className="lg:col-span-2 bg-gray-800 p-6 rounded-xl shadow-2xl">
            <h2 className="text-2xl font-bold mb-4 border-b border-gray-700 pb-2 text-cyan-400">Diagnostic Report</h2>
            <div className="report-content h-[400px] md:h-[500px] text-gray-300 overflow-y-auto pr-2">
                {error && (
                  <div className="bg-red-900/50 border border-red-700 text-red-300 p-4 rounded-lg">
                    <p className="font-bold">Error</p>
                    <p>{error}</p>
                  </div>
                )}
                {!error && !isLoading && !analysisResult && (
                  <div className="flex items-center justify-center h-full text-gray-500">
                      <p>Analysis results will appear here.</p>
                  </div>
                )}
                {isLoading && (
                    <div className="flex flex-col items-center justify-center h-full text-gray-500">
                        <Spinner />
                        <p className="mt-4">Generating report...</p>
                    </div>
                )}
                
                {analysisResult && (
                  // Use ReactMarkdown to render the report correctly
                  <article className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown>
                      {analysisResult.report}
                    </ReactMarkdown>
                  </article>
                )}
            </div>
          </div>
        </div>

        <footer className="text-center mt-12 text-gray-500 text-sm">
            <p>Powered by FastAPI, React, and Roboflow. For educational purposes only.</p>
        </footer>
      </div>
    </div>
  );
};

export default App;
