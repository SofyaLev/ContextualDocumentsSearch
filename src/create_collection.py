import chromadb
import os

def Create_collection(text_chunks, docname):
    app_data_path = os.path.join(os.environ.get('LOCALAPPDATA', 'C:\\Temp'), 'ChromaDBDocStorage')
    os.makedirs(app_data_path, exist_ok=True)
    client = chromadb.PersistentClient(path = app_data_path)
    collection = client.get_or_create_collection(name=docname)
    collection.add(
    documents=text_chunks,
    ids=[f'{x}' for x in range(len(text_chunks))])
    return collection