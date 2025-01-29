1. Create a Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

macOS/Linux

python3 -m venv venv
source venv/bin/activate

2. Install Dependencies

pip install -r requirements.txt

3. Set Up Environment Variables

Create a .env file and add the following:

OPENAI_API_KEY=your_openai_api_key
DATA_DIR=/path/to/bbc-news-data
CHROMADB_PATH=chromadb_store

Running the Chatbot

1. Store Embeddings

Run the Streamlit app, and click the "Store Embeddings in Both Collections" button before querying.

2. Start the Streamlit App

streamlit run app.py

