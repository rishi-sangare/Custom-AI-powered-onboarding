import streamlit as st
from utils import extract_text_from_pdf, extract_text_from_url, query_openai

# Initialize session state for questions and questionnaire
if "questions" not in st.session_state:
    st.session_state.questions = [
        "What is the job title?",
        "What are the required skills?",
        "What is the job location?",
        "What is the salary range (if mentioned)?",
        "Describe the interview process."
    ]
if "questionnaire" not in st.session_state:
    st.session_state.questionnaire = {}

# Streamlit UI
st.title("AI-Powered Job Onboarding")

st.header("Upload Job Description or Enter URL")
input_type = st.radio("Choose Input Type", ["PDF Upload", "URL"])

# File Upload or URL Input
if input_type == "PDF Upload":
    uploaded_file = st.file_uploader("Upload PDF File", type=["pdf"])
elif input_type == "URL":
    url_input = st.text_input("Enter Job Description URL")

# Extracted Content Display
if st.button("Extract and Generate Questionnaire"):
    if input_type == "PDF Upload" and uploaded_file:
        with st.spinner("Processing PDF..."):
            extracted_text = extract_text_from_pdf(uploaded_file)
    elif input_type == "URL" and url_input:
        with st.spinner("Processing URL..."):
            extracted_text = extract_text_from_url(url_input)
    else:
        st.error("Please upload a file or provide a valid URL.")
        st.stop()

    # Use OpenAI API to generate answers
    with st.spinner("Using AI to generate questionnaire..."):
        st.session_state.questionnaire = query_openai(
            extracted_text, st.session_state.questions
        )

    st.success("Questionnaire generated successfully!")

# Editable Questionnaire Section
st.subheader("Editable Questionnaire")
questions_to_delete = []

# Dynamically generate editable questions and answers
for idx, question in enumerate(st.session_state.questions):
    col1, col2 = st.columns([4, 1])
    with col1:
        # Edit the question and its answer
        updated_question = st.text_input(
            f"Question {idx + 1}", value=question, key=f"question_{idx}"
        )
        if updated_question != st.session_state.questions[idx]:
            st.session_state.questions[idx] = updated_question

        st.session_state.questionnaire[updated_question] = st.text_area(
            f"Answer {idx + 1}",
            value=st.session_state.questionnaire.get(updated_question, ""),
            height=100,
            key=f"answer_{idx}",
        )
    with col2:
        # Add a delete button for each question
        if st.button("Delete", key=f"delete_{idx}"):
            questions_to_delete.append(idx)

# Remove deleted questions
if questions_to_delete:
    for idx in sorted(questions_to_delete, reverse=True):
        del st.session_state.questions[idx]
        st.session_state.questionnaire.pop(st.session_state.questions[idx], None)

# Add New Question
new_question = st.text_input("Add a New Question", key="new_question")
if st.button("Add Question"):
    if new_question:
        st.session_state.questions.append(new_question)
        st.session_state.questionnaire[new_question] = ""
        st.success("New question added!")

# Re-run OpenAI API Call
if st.button("Re-run AI Processing"):
    if input_type == "PDF Upload" and uploaded_file:
        extracted_text = extract_text_from_pdf(uploaded_file)
    elif input_type == "URL" and url_input:
        extracted_text = extract_text_from_url(url_input)
    else:
        st.error("Please upload a file or provide a valid URL.")
        st.stop()

    with st.spinner("Re-running AI processing..."):
        # Fetch updated answers
        updated_questionnaire = query_openai(
            extracted_text, st.session_state.questions
        )
        # Update the questionnaire with new answers
        for question in st.session_state.questions:
            st.session_state.questionnaire[question] = updated_questionnaire.get(
                question, ""
            )

    st.success("Re-run completed successfully!")
