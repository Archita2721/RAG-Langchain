# 📚 BBC News RAG Chatbot with ChromaDB & OpenAI 🚀

This project implements a **Retrieval-Augmented Generation (RAG) chatbot** that answers questions based on BBC news articles. It uses **ChromaDB** for vector storage and **OpenAI's embeddings** to store and retrieve relevant text.

## 🔥 Features
- ✅ **Fast Processing** - Uses parallel processing for fast embedding storage  
- ✅ **Automatic Detection of Stored Embeddings** - Avoids redundant storage  
- ✅ **Delete & Refresh Embeddings** - User can manually update vector storage  
- ✅ **Hybrid Chunking** - Supports both **fixed-size and semantic chunking**  
- ✅ **Efficient Vector Search** - Retrieves top relevant document chunks for answering queries  

---

## ⚙️ Tech Stack
- **Python** 🐍
- **Streamlit** - Interactive UI
- **OpenAI API** - Text embeddings & GPT-based responses
- **ChromaDB** - Vector database
- **LangChain** - Text chunking & retrieval

---

## 🚀 Installation & Setup

### 1️⃣ Clone Repository
```sh
git clone https://github.com/your-repo/bbc-news-rag.git
cd bbc-news-rag
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file and add the following:
```ini
OPENAI_API_KEY=your_openai_api_key
DATA_DIR=/path/to/bbc-news-dataset
CHROMADB_PATH=chromadb_store
```

### 5️⃣ Run the Streamlit App
```sh
streamlit run app.py
```

---

## 🏢 Project Structure
```
bbc-news-rag/
️️ backend/
│   │── __init__.py
│   │── data_loader.py          # Loads BBC news data
│   │── embedding.py            # Text chunking & embeddings
│   │── retrieval.py            # Vector storage & retrieval
│   │── response_generator.py   # Generates answers using GPT
│── config.py                   # Loads environment variables
│── app.py                      # Streamlit UI
│── requirements.txt             # Required Python packages
│── README.md                    # Project documentation
│── .env                         # Environment variables (not committed)
```

---

## 🔥 How It Works
### **1️⃣ Store Embeddings**
- Loads BBC news articles
- Chunks text using **fixed-size & semantic chunking**
- Stores embeddings in **ChromaDB**

### **2️⃣ Ask Questions**
- Retrieves **most relevant document chunks**
- Passes them to **GPT-4** for response generation
- Displays the answer in Streamlit UI

---

## 📀 Key Optimizations
| **Optimization** | **Before** ⏳ | **After 🚀** |
|-----------------|--------------|--------------|
| **Embedding Storage** | **Sequential (1hr)** | **Parallel (10-15 min)** |
| **Batch OpenAI Calls** | ❌ No | ✅ Yes |
| **ChromaDB Write Speed** | ❌ Slow | ✅ Optimized |
| **Old Embeddings Cleanup** | ❌ Manual | ✅ Automatic |

---

## 🔥 Usage
### **Storing Embeddings**
- If embeddings already exist, the chatbot allows **direct questioning**.
- If embeddings need to be refreshed, click **"Delete & Store New Embeddings"**.

### **Asking Questions**
- Choose a **retrieval method**: `normal` (fixed-size) or `semantic`.
- Enter a question → Click **"Search"** → Get an answer!

---

## 🛠️ Troubleshooting
#### **Q: OpenAI API error?**
✅ Ensure your `.env` file has a valid `OPENAI_API_KEY`.

#### **Q: Embeddings not storing?**
✅ Make sure `CHROMADB_PATH` points to a **writable directory**.

#### **Q: Slow processing?**
✅ Increase `max_workers` in `retrieval.py` (default is `5`).

---

## 🏆 Contributing
Feel free to **fork** this repo, **open issues**, and contribute via **pull requests**! 🚀

---

## 🐝 License
MIT License. Free to use, modify, and distribute. 🎉

---

## 📩 Contact
For any questions or collaborations, contact [Archita Shah] at [architashah27@gmail.com]. 😊