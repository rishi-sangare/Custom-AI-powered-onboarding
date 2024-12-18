from openai import OpenAI
client = OpenAI()
import PyPDF2
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_url(url):
    """Extract text content from a URL."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n")
    else:
        return "Failed to retrieve content."

def query_openai(text, questions):
    """Use OpenAI GPT API to extract answers for given questions."""
    prompt = f"The following text is a job description:\n\n{text}\n\n"
    prompt += "Answer the following questions based on the job description:\n"
    for i, question in enumerate(questions, 1):
        prompt += f"{i}. {question}\n"

    # Use ChatCompletion for GPT models
    response = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo" if you prefer
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the actual text content from the message
    answer_text = response.choices[0].message.content
    
    # You might want to split the answers manually or use a more sophisticated parsing method
    answers = answer_text.split('\n')
    
    # Create a dictionary mapping questions to their answers
    return {q: ans.strip() for q, ans in zip(questions, answers) if ans.strip()}

