import boto3
from botocore.exceptions import ClientError
import json
from pypdf import PdfReader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize AWS Bedrock client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Simulated in-memory store for demonstration purposes
text_store = {}
embedding_store = {}

# Embed text function
def embed_text(text):
    model_id = "amazon.titan-embed-text-v2:0"
    body = {
        "inputText": text,
        "dimensions": 512,
        "normalize": True
    }

    try:
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )
        response_data = json.loads(response["body"].read().decode("utf-8"))
        embedding = response_data.get("embedding", None)
        if embedding is None:
            print(f"ERROR: No embedding found in response from '{model_id}'.")
        return embedding

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return None

# Store text and embedding
def store_text_and_embedding(key, text, embedding):
    text_store[key] = text
    embedding_store[key] = embedding

# Retrieve relevant texts based on query embedding
def retrieve_relevant_texts(query_embedding, top_k=5):
    all_embeddings = list(embedding_store.values())
    all_keys = list(embedding_store.keys())
    
    if not all_embeddings:
        return []

    all_embeddings = np.array(all_embeddings)
    query_embedding = np.array(query_embedding).reshape(1, -1)
    similarities = cosine_similarity(query_embedding, all_embeddings)
    
    # Get indices of the top_k most similar embeddings
    top_indices = np.argsort(similarities[0])[-top_k:]
    return [all_keys[i] for i in top_indices]

# Perform question answering using the model
def perform_question_answering(prompt_text):
    model_id = "meta.llama3-70b-instruct-v1:0"
    body = {
        "prompt": prompt_text,
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }

    try:
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body),
        )
        response_data = json.loads(response["body"].read().decode("utf-8"))

        # Extract generated text from response
        response_text = response_data.get("generation", None)
        if response_text is None or not response_text.strip():
            print("ERROR: No generated text found in response from the model.")
            return []

        # Split the response text into individual questions, filtering out non-question content
        lines = response_text.strip().split('\n')
        questions = [line.strip() for line in lines if line.strip() and not line.startswith(('**', 'Here are some questions'))]

        return questions

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        return []

# Extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"ERROR: Unable to extract text from PDF. Reason: {e}")
        return ""

# Example usage
pdf_file_path = "resume/resume.pdf"  # Update with the actual file name
resume_text = extract_text_from_pdf(pdf_file_path)

if resume_text.strip():
    # Embed and store the resume text and embedding
    resume_embedding = embed_text(resume_text)
    if resume_embedding is not None:
        store_text_and_embedding("resume", resume_text, resume_embedding)
    
    # Retrieve relevant context based on a query (e.g., question prompt)
    query_prompt = "Generate questions related to skills and projects based on the following content:"
    query_text = f"{query_prompt} {resume_text}"
    query_embedding = embed_text(query_text)
    
    if query_embedding is not None:
        relevant_keys = retrieve_relevant_texts(query_embedding)
        # Use relevant_keys to fetch actual texts
        context_text = " ".join([text_store[key] for key in relevant_keys])
        
        # Perform question answering
        questions_prompt = f"""
        Based on the following resume content and context, generate questions related to skills and projects:
        
        Resume Content: {resume_text}
        Context: {context_text}
        
        Please provide questions that would help evaluate the candidate's skills and projects.
        """
        
        questions = perform_question_answering(questions_prompt)
        
        if questions:
            # Print only the list of questions
            print(json.dumps(questions, indent=2))
        else:
            print("ERROR: No questions generated. Please check the prompt or model response.")
    
else:
    print("ERROR: The extracted text from the PDF is empty. Please check the PDF content.")
