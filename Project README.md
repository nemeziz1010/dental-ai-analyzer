Dental AI Analyzer 🦷✨

Replace this URL with a link to one of your screenshots showing the final result.

A full-stack web application that analyzes dental X-ray (DICOM) images to detect pathologies using AI and generates a professional diagnostic report.
🌟 Key Features
🦷 DICOM File Processing: Securely upload and process standard .dcm and .rvg dental X-ray files.

🤖 AI-Powered Detection: Utilizes a Roboflow object detection model to accurately identify cavities and periapical lesions.

🎨 Dynamic Annotations: Overlays precise, color-coded bounding boxes on the X-ray to visually highlight detected issues.

✍️ LLM-Generated Reports: Leverages the OpenAI GPT API to generate structured, human-readable diagnostic reports in clinical language.

🖥️ Responsive UI: A modern, clean, two-panel interface built with React and Tailwind CSS for a seamless experience on any device.

🔒 Secure & Robust Backend: Built with FastAPI, featuring asynchronous operations and clear, structured error handling.

🛠️ Tech Stack & Architecture
Technologies Used
Architecture Diagram
(This is a simplified view of the application's data flow)


Replace this URL with a link to a simple diagram showing the flow: Frontend -> Backend -> AI APIs -> Backend -> Frontend.

🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

Prerequisites
Python 3.11+

Node.js v18+ and npm

Git

1. Clone the Repository
git clone [https://github.com/](https://github.com/)[YOUR_GITHUB_USERNAME]/dental-ai-analyzer.git
cd dental-ai-analyzer

2. Configure API Keys
Create a .env file in the root directory by copying the example file (.env.example). If you don't have an example file, create one with the content below.

# This command works if you have .env.example
cp .env.example .env

Important: Open the .env file and add your private API keys from Roboflow and OpenAI.

ROBOFLOW_API_KEY="YOUR_ROBOFLOW_API_KEY_HERE"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"

3. Backend Setup (Terminal 1)
The backend server runs on port 8000.

# Create and activate a virtual environment from the project root
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload

4. Frontend Setup (Terminal 2)
The frontend application runs on port 5173.

# Navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the frontend development server
npm run dev

✅ How to Use
Once both servers are running:

Open your browser and navigate to http://localhost:5173.

Click "Select DICOM File" and choose a .dcm or .rvg file.

Click "Analyze Image".

Observe the annotated image in the left panel and the AI-generated diagnostic report in the right panel.