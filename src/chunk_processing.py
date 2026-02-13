from src.text_extration import TextExtraction
import re


def find_best_chunk(collection, request):
    request = TextExtraction.lemmatization_and_punct_clean(request)
    results = collection.query(
        query_texts=[f'{request}'],
        n_results=1
    )
    best_distance = results['distances'][0][0]
    best_chunk = results['documents'][0][0]

    return best_chunk, best_distance


def chunk_text_by_sentence(text: str, n: int):
    sentences = re.split(r'(?<=[.?!])\s+', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > n and current_chunk:
            current_chunk += sentence + " "
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
        else:
            current_chunk += sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
