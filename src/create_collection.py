from pathlib import Path
import uuid
import chromadb
import os
from find_best_function import find_best_chunk
from text_extration import TextExtraction
from chunking import chunk_text_by_sentence

app_data_path = os.path.join(os.environ.get('LOCALAPPDATA', 'C:\\Temp'), 'ChromaDBDocStorage')
os.makedirs(app_data_path, exist_ok=True)
client = chromadb.PersistentClient(path=app_data_path)
request = 'кошка'


def create_collection(text_chunks, relative_path):
    collection = client.get_or_create_collection(name=str(uuid.uuid4()))
    collection.upsert(
        documents = text_chunks,
        ids = [f'{x}' for x in range(len(text_chunks))],
        metadatas=[{'path': str(relative_path)} for _ in range(len(text_chunks))]
    )
    return collection


def create_documents_collections(current_folder):
    documents_dict = TextExtraction(current_folder).extract() # {'path': 'text', ...}
    distances = {}
    for path in documents_dict:
        text = documents_dict[path]
        n = 400
        chunks = chunk_text_by_sentence(text, n)
        collection = create_collection(chunks, path)
        best_chunk, best_distance = find_best_chunk(collection, request)
        distances[path] = best_distance
    return distances


main_folder_name = 'documents'  # название корневого каталога
main_folder = Path.joinpath(Path(__file__).parent.parent, main_folder_name)  # полный путь до корневого каталога

d = create_documents_collections(main_folder)
print(d)


