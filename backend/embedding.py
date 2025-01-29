from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
import config

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)

def chunk_text_normal(text, chunk_size=512, overlap=128):
    """Chunk text into fixed-size segments with overlap."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    return splitter.split_text(text)

def chunk_text_semantic(text):
    """Chunk text using semantic chunking."""
    text_splitter = SemanticChunker(OpenAIEmbeddings(api_key=config.OPENAI_API_KEY))
    docs = text_splitter.create_documents([text])
    return [doc.page_content for doc in docs]

def embed_text(texts):
    """Generate embeddings using OpenAI's API."""
    if isinstance(texts, str):
        texts = [texts]

    texts = [t.strip() for t in texts if isinstance(t, str) and t.strip()]
    if not texts:
        raise ValueError("Input to embeddings cannot be empty or invalid.")

    response = client.embeddings.create(input=texts, model="text-embedding-ada-002")
    return [embedding.embedding for embedding in response.data]
