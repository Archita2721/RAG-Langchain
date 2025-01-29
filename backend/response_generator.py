from backend.retrieval import retrieve_relevant_chunks
from openai import OpenAI
import config
from constants import OPENAI_MODEL

client = OpenAI(api_key=config.OPENAI_API_KEY)

def generate_answer(query, chunking_type):
    """Generate an answer using OpenAI's GPT model."""
    relevant_chunks = retrieve_relevant_chunks(query, chunking_type)

    if not relevant_chunks or not relevant_chunks[0]:
        return "No relevant information found."

    context = "\n".join(relevant_chunks[0])
    
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI answering BBC news-related questions."},
            {"role": "user", "content": f"Context: {context}\nQuestion: {query}"}
        ]
    )

    return response.choices[0].message.content
