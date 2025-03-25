import gradio as gr
import pandas as pd
import json
from PyPDF2 import PdfReader
import tempfile
import google.generativeai as genai
import docx  
import re

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# 📌 **Extract text from PDFs**
def extract_text_from_pdf(file):
    """Extracts text from a PDF file."""
    pdf = PdfReader(file)
    text = "\n".join([page.extract_text().strip() or "" for page in pdf.pages])
    return text if text.strip() else "No readable text found."

# 📌 **Extract text from DOCX files**
def extract_text_from_docx(file):
    """Extracts text from a DOCX file."""
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text if text.strip() else "No readable text found."

# 📌 **Process multiple resumes**
def process_resumes(files):
    """Extracts text from multiple PDFs and DOCX files."""
    resumes = []
    for file in files:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            continue  # Ignore unsupported formats

        resumes.append({"name": file.name, "text": text})
    
    return resumes

# 📌 **Rank Resumes using Gemini AI**
def rank_resumes(job_description, resume_files):
    """Rank resumes based on job description."""
    if not resume_files:
        return pd.DataFrame(columns=["name", "score"])  # No files provided
    
    resumes = []
    for file in resume_files:
        if file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            text = extract_text_from_docx(file)
        else:
            continue  # Skip unsupported formats
        resumes.append({"name": file.name, "text": text})

    if not resumes:
        return pd.DataFrame(columns=["name", "score"])  # No valid files

    # Format input for Gemini API
    prompt = f"""
    You are an AI assistant ranking resumes based on job descriptions. Here is the job description:

    {job_description}

    Below are the resumes of candidates. Assign a relevance score (0-100) based on how well they match the job description.
    Return results in valid JSON format: 
    [{{"name": "resume1.pdf", "score": 85}}, ...]
    
    Resumes:
    {resumes}
    """

    response = model.generate_content(prompt)

    # Extract JSON safely
    cleaned_response = re.search(r"\[\{.*\}\]", response.text, re.DOTALL)
    if cleaned_response:
        ranked_results = json.loads(cleaned_response.group())  # Extract valid JSON
        ranked_df = pd.DataFrame(ranked_results).sort_values(by="score", ascending=False)
        return ranked_df
    else:
        return pd.DataFrame(columns=["name", "score"])  # Return empty DataFrame if parsing fails

# 📌 **Generate Downloadable CSV**
def download_results(job_description, resume_files):
    """Creates a CSV file with ranked resumes."""
    ranking_results = rank_resumes(job_description, resume_files)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    ranking_results.to_csv(temp_file.name, index=False)
    return temp_file.name

# 📌 **Gradio UI**
with gr.Blocks() as app:
    gr.Markdown("# 🚀 AI Resume Ranking System (Powered by Gemini)")

    with gr.Row():
        job_desc_input = gr.Textbox(lines=5, placeholder="Enter job description...", label="📝 Job Description")
        resume_upload = gr.File(file_types=[".pdf", ".docx"], label="📤 Upload Resumes", file_count="multiple")

    rank_button = gr.Button("🔍 Rank Resumes")
    download_button = gr.Button("⬇️ Download CSV")

    results_output = gr.Dataframe(label="📊 Ranked Resumes")
    download_output = gr.File(label="Download CSV")

    rank_button.click(rank_resumes, inputs=[job_desc_input, resume_upload], outputs=results_output)
    download_button.click(download_results, inputs=[job_desc_input, resume_upload], outputs=download_output)

# 📌 **Launch App**
app.launch(server_name="0.0.0.0", server_port=7860, share=True)
