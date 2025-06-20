# 🦷 Dental AI Analyzer ✨

![Screenshot](REPLACE_WITH_YOUR_SCREENSHOT_URL)

A full-stack web application that analyzes dental X-ray (DICOM) images to detect pathologies using AI and generates a formal diagnostic report in clinical language.

---

## 🌟 Key Features

- 🦷 **DICOM File Processing**  
  Upload and analyze standard `.dcm` and `.rvg` dental X-ray files securely.

- 🤖 **AI-Powered Detection**  
  Utilizes a Roboflow object detection model to identify **cavities** and **periapical lesions** with high confidence.

- 🎨 **Dynamic Annotations**  
  Visual overlays (color-coded bounding boxes) highlight detected regions on the radiograph.

- ✍️ **LLM-Generated Reports**  
  OpenAI GPT API creates professional, human-readable diagnostic reports for clinical use.

- 🖥️ **Responsive UI**  
  Clean two-panel interface built with **React** and **Tailwind CSS**, optimized for desktops and tablets.

- 🔒 **Secure Backend**  
  FastAPI-based backend with asynchronous inference calls, structured error handling, and API key safety via `.env`.

---

## 🛠️ Tech Stack & Architecture

**Frontend:** React, Tailwind CSS  
**Backend:** FastAPI, Python 3.11+  
**AI Services:** Roboflow Detection API, OpenAI GPT-3.5  
**Data Format:** DICOM (.dcm/.rvg)  
**Communication:** REST APIs  
**Others:** Base64 Image Handling, Markdown Reports

### 🧭 Architecture Diagram

```plaintext
User
 |
 v
Frontend (React + Tailwind)
 |
 v
Backend (FastAPI)
 |
 v
+------------------------+
| Roboflow Detection API |
+------------------------+
| OpenAI GPT API         |
+------------------------+
 |
 v
Backend ➝ Frontend ➝ UI (Report + Annotated Image)
🚀 Getting Started
Follow these steps to set up and run the project locally.
```
✅ Prerequisites
Python 3.11+

Node.js v18+ and npm

Git

1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/YOUR_GITHUB_USERNAME/dental-ai-analyzer.git
cd dental-ai-analyzer
2. Configure API Keys
Create a .env file in the project root. You can use the .env.example if available:

bash
Copy
Edit
cp .env.example .env
Edit the .env file and add:

env
Copy
Edit
ROBOFLOW_API_KEY="your_roboflow_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
3. Backend Setup (Terminal 1)
bash
Copy
Edit
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server (default port: 8000)
uvicorn main:app --reload
4. Frontend Setup (Terminal 2)
bash
Copy
Edit
cd frontend

# Install frontend dependencies
npm install

# Run development server (default port: 5173)
npm run dev
✅ How to Use
Open your browser and visit: http://localhost:5173

Click "Select DICOM File" and upload a .dcm or .rvg file.

Click "Analyze Image".

View:

Annotated X-ray (left panel)

AI-generated diagnostic report (right panel)

📸 Screenshots
Replace this with your image or link:

🧠 Sample Report Preview
markdown
Copy
Edit
**Findings:**
- A cavity detected with 85% confidence on the right side.
- A periapical abscess detected with 84% confidence on the right side.

**Interpretation:**
- The cavity suggests a localized area of decay.
- The periapical abscess may indicate root infection.

**Recommendations:**
- Consider immediate dental filling and abscess drainage.

**Disclaimer:** This is an AI-generated report for educational purposes only. All findings must be clinically validated.
🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

📄 License
This project is licensed under the MIT License.

🙏 Acknowledgements
Roboflow

OpenAI

FastAPI

React
