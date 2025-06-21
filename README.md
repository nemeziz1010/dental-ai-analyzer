# 🦷 Dental AI Analyzer ✨

> A full-stack web application that analyzes dental X-ray (DICOM) images to detect pathologies using AI and generates a professional diagnostic report.

---

## 🌟 Key Features

-  **DICOM File Processing**  
  Securely upload and process standard `.dcm` and `.rvg` dental X-ray files.

-  **AI-Powered Detection**  
  Utilizes a Roboflow object detection model to accurately identify cavities and periapical lesions.

-  **Dynamic Annotations**  
  Overlays precise, color-coded bounding boxes on the X-ray to visually highlight detected issues.

-  **LLM-Generated Reports**  
  Leverages the OpenAI API (using the **GPT-4** model) to generate structured, human-readable diagnostic reports in clinical language.

-  **Responsive UI**  
  A modern, clean, two-panel interface built with React and Tailwind CSS for a seamless experience on any device.

-  **Secure & Robust Backend**  
  Built with FastAPI, featuring asynchronous operations and structured error handling.
  
-  **Dockerized Deployment**  
  Easily portable and consistent development and production environments using Docker containers.
  
---

## 🛠️ Tech Stack & Architecture

**Frontend:** React, Tailwind CSS  
**Backend:** FastAPI, Python 3.11+  
**Containerization:** Docker   
**AI Services:** Roboflow API, OpenAI GPT-4.0  
**Data Format:** DICOM (.dcm/.rvg)  
**Architecture Flow:**  
*Frontend ➝ Backend (Dockerized) ➝ AI APIs (Roboflow + OpenAI) ➝ Backend ➝ Frontend*



---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js v18+ and npm
- Docker Desktop (for containerized setup)

---

### 1. Clone the Repository

```bash
git clone https://github.com/nemeziz1010/dental-ai-analyzer.git
cd dental-ai-analyzer
```

---

### 2. Configure API Keys

Create a `.env` file in the root directory. You can copy it from `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file and add:

```env
ROBOFLOW_API_KEY="YOUR_ROBOFLOW_API_KEY_HERE"
OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"
```

---

### 3. **Build and Run:**

Make sure Docker Desktop is running, then execute:
```bash
docker compose up --build
```

### 4. **Access the App:**

Open your browser and navigate to `http://localhost`.

---

### Option 2: Running Locally (Without Docker)
Follow these steps if you prefer to run the frontend and backend servers directly on your machine.

1. **Clone & Configure:**

Follow steps 1 and 2 from the Docker setup above.

2. **Backend Setup (Terminal 1):**
```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
uvicorn main:app --reload
```

3. **Frontend Setup (Terminal 2):**
```bash
# Navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the frontend development server
npm run dev
```

You can now access the app at `http://localhost:5173`.

---

## How to Use

1. Open your browser and go to [http://localhost](http://localhost)
2. Click **"Select DICOM File"** and choose a `.dcm` or `.rvg` file.
3. Click **"Analyze Image"**.
4. View the **annotated X-ray** on the left and the **AI-generated report** on the right.

---

## Screenshots
![App screenshot](./frontend/readme%20images/main.png)

---

## Acknowledgements

- [Roboflow](https://roboflow.com)
- [OpenAI](https://openai.com)
- [FastAPI](https://fastapi.tiangolo.com)
- [React](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
