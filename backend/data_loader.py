import os

def load_bbc_data(data_dir):
    """Load BBC news text data."""
    documents = []
    metadata = []
    categories = os.listdir(data_dir)
    for category in categories:
        category_path = os.path.join(data_dir, category)
        if os.path.isdir(category_path):
            for file in os.listdir(category_path):
                file_path = os.path.join(category_path, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
                    documents.append(text)
                    metadata.append({"category": category, "file": file})
    return documents, metadata
