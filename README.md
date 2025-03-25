# 🚀 AI Resume Ranking System 

An AI-powered web application that ranks resumes based on a given job description using **Google Gemini API**.

📌 Features
- Extracts text from PDFs and DOCX resumes
- Uses **Google Gemini AI** to rank resumes based on job descriptions
- Provides a downloadable CSV of ranked results
- Built using **Gradio** for a simple and interactive UI

## 🛠 Technologies Used
- **Python**
- **Gradio** (UI)
- **PyPDF2** (Extract text from PDFs)
- **python-docx** (Extract text from DOCX)
- **Google Gemini API** (For resume ranking)
- **Pandas** (For data processing)

## 🔧 Installation & Running Locally

1️⃣ Clone the Repository

git clone https://github.com/your-username/AI-Resume-Ranking.git
cd AI-Resume-Ranking

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Set Up Google Gemini API
    GEMINI_API_KEY=your_api_key_here
    #insert your gemini api key here
    
4️⃣ Run the Application
open the terminal and type
    python ranker.py


🔥 Gemini API Prompt Structure:


You are an AI assistant ranking resumes based on job descriptions. Here is the job description:

{job_description}

Below are the resumes of candidates. Assign a relevance score (0-100) based on how well they match the job description.
Return results in valid JSON format:
[{"name": "resume1.pdf", "score": 85}, ...]



