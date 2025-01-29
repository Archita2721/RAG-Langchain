
# import streamlit as st
# from backend.data_loader import load_bbc_data
# from backend.retrieval import store_embeddings_in_chromadb, get_chromadb_client
# from backend.response_generator import generate_answer
# import config

# st.title("BBC News RAG Chatbot")

# # Function to check if embeddings already exist
# def check_existing_embeddings():
#     client = get_chromadb_client()
#     normal_collection = client.get_or_create_collection(name="bbc_news_normal")
#     semantic_collection = client.get_or_create_collection(name="bbc_news_semantic")

#     # Check if collections have any stored documents
#     return normal_collection.count() > 0 and semantic_collection.count() > 0

# def delete_existing_embeddings():
#     client = get_chromadb_client()
#     normal_collection = client.get_or_create_collection(name="bbc_news_normal")
#     semantic_collection = client.get_or_create_collection(name="bbc_news_semantic")

#     # Fetch all document IDs
#     normal_docs = normal_collection.get()
#     semantic_docs = semantic_collection.get()

#     normal_ids = normal_docs.get("ids", [])
#     semantic_ids = semantic_docs.get("ids", [])

#     # Delete documents only if there are stored IDs
#     if normal_ids:
#         normal_collection.delete(ids=normal_ids)
#     if semantic_ids:
#         semantic_collection.delete(ids=semantic_ids)

#     st.success("All previous embeddings have been deleted!")

# # Load BBC data
# documents, metadata = load_bbc_data(config.DATA_DIR)

# # Detect stored embeddings
# if "embeddings_stored" not in st.session_state:
#     st.session_state.embeddings_stored = check_existing_embeddings()

# # Section to re-store embeddings
# st.write("### Embedding Management")
# if st.session_state.embeddings_stored:
#     st.write("✅ **Embeddings are already stored!** You can ask questions directly.")
    
#     # Button to re-store embeddings (deletes old ones first)
#     if st.button("Delete & Store New Embeddings"):
#         with st.spinner("Deleting old embeddings..."):
#             delete_existing_embeddings()
        
#         with st.spinner("Storing new embeddings... This may take a few minutes."):
#             store_embeddings_in_chromadb(documents, metadata)
        
#         st.session_state.embeddings_stored = True
#         st.success("New embeddings stored successfully!")
# else:
#     if st.button("Store Embeddings"):
#         with st.spinner("Storing embeddings... This may take a few minutes."):
#             store_embeddings_in_chromadb(documents, metadata)
#         st.session_state.embeddings_stored = True
#         st.success("Embeddings stored successfully! You can now ask questions.")

# # Allow questions only if embeddings exist
# if st.session_state.embeddings_stored:
#     st.write("### Ask a Question")
#     chunking_type = st.selectbox("Select Retrieval Method", ["normal", "semantic"])
#     query = st.text_input("Ask a question about BBC news articles:")

#     if st.button("Search"):
#         if query:
#             answer = generate_answer(query, chunking_type)
#             st.write("### Answer:")
#             st.write(answer)
#         else:
#             st.warning("Please enter a query.")
# else:
#     st.warning("Please store embeddings before asking questions.")


import streamlit as st
from backend.data_loader import load_bbc_data
from backend.retrieval import store_embeddings_in_chromadb, get_chromadb_client, delete_existing_embeddings
from backend.response_generator import generate_answer
import config

st.title("BBC News RAG Chatbot")

# Function to check if embeddings exist
def check_existing_embeddings():
    client = get_chromadb_client()
    normal_collection = client.get_or_create_collection(name="bbc_news_normal")
    semantic_collection = client.get_or_create_collection(name="bbc_news_semantic")

    return normal_collection.count() > 0 and semantic_collection.count() > 0

# Load BBC data
documents, metadata = load_bbc_data(config.DATA_DIR)

# Detect stored embeddings
if "embeddings_stored" not in st.session_state:
    st.session_state.embeddings_stored = check_existing_embeddings()

# Embedding Management
st.write("### Embedding Management")

if st.session_state.embeddings_stored:
    st.write("✅ **Embeddings are already stored!** You can ask questions directly.")

    if st.button("Delete & Store New Embeddings"):
        with st.spinner("Deleting old embeddings..."):
            delete_existing_embeddings()

        with st.spinner("Storing new embeddings... This may take a few minutes."):
            store_embeddings_in_chromadb(documents, metadata)

        st.session_state.embeddings_stored = True
        st.success("New embeddings stored successfully!")
else:
    if st.button("Store Embeddings"):
        with st.spinner("Storing embeddings... This may take a few minutes."):
            store_embeddings_in_chromadb(documents, metadata)
        st.session_state.embeddings_stored = True
        st.success("Embeddings stored successfully! You can now ask questions.")

# Question-Answering Section
if st.session_state.embeddings_stored:
    st.write("### Ask a Question")
    chunking_type = st.selectbox("Select Retrieval Method", ["normal", "semantic"])
    query = st.text_input("Ask a question about BBC news articles:")

    if st.button("Search"):
        if query:
            answer = generate_answer(query, chunking_type)
            st.write("### Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a query.")
else:
    st.warning("Please store embeddings before asking questions.")
