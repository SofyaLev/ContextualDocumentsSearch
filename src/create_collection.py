from pathlib import Path
import re
import chromadb
import os
from find_best_function import find_best_chunk
from text_extration import TextExtraction
from chunking import chunk_text_by_sentence
import nltk

nltk.download('punkt_tab')
nltk.download('wordnet')

class RelevantDocumentsSearch:
    def __init__(self, current_folder_path, request, chunk_length=400):
        self.app_data_path = os.path.join(os.environ.get('LOCALAPPDATA', 'C:\\Temp'), 'ChromaDBDocStorage')
        os.makedirs(self.app_data_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.app_data_path)
        self.request = request
        self.current_folder_path = current_folder_path
        self.chunk_length = chunk_length


    def create_collection(self, text_chunks, relative_path):
        parts = re.split(r'[/\\]', str(relative_path))
        name_str = '.'.join(parts)
        collection = self.client.get_or_create_collection(name=name_str)
        text_chunks_lemmed = []
        for chunk in text_chunks:
            chunk = TextExtraction.lemmatization_and_punct_clean(chunk)
            text_chunks_lemmed.append(chunk)
        collection.upsert(
            documents = text_chunks_lemmed,
            ids = [f'{x}' for x in range(len(text_chunks_lemmed))],
            metadatas=[{'path': str(relative_path)} for _ in range(len(text_chunks_lemmed))]
        )
        return collection


    def find_documents(self) -> dict:
        documents_dict = TextExtraction(self.current_folder_path).extract()  # {'path': 'text', ...}
        distances = {}
        for path in documents_dict:
            text = documents_dict[path]
            chunks = chunk_text_by_sentence(text, self.chunk_length)
            collection = self.create_collection(chunks, path)
            best_chunk, best_distance = find_best_chunk(collection, self.request)
            distances[path] = best_distance
        return distances


main_folder_name = 'documents'  # название корневого каталога
main_folder = Path.joinpath(Path(__file__).parent.parent, main_folder_name)  # полный путь до корневого каталога

d = RelevantDocumentsSearch(main_folder, 'я повесил пиджак на стул').find_documents()
sorted_d = dict(sorted(d.items(), key=lambda x: x[1]))
print(sorted_d)