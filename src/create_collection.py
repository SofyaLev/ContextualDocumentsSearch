import chromadb
import os

from src.text_extration import TextExtraction

app_data_path = os.path.join(os.environ.get('LOCALAPPDATA', 'C:\\Temp'), 'ChromaDBDocStorage')
os.makedirs(app_data_path, exist_ok=True)
client = chromadb.PersistentClient(path=app_data_path)


def create_collection(text_chunks, relative_path):
    collection = client.get_or_create_collection(name=relative_path)
    collection.upsert(
        documents = text_chunks,
        ids = [f'{x}' for x in range(len(text_chunks))])
    return collection


def create_documents_collections(current_folder):
    documents_dict = TextExtraction(current_folder).texts
    for path in documents_dict:
        return create_collection(chunking(documents_dict[path]), path)


def chunking(text) -> list:
    pass


def find_document(path, request):
    create_documents_collections(path)


