from text_extration import TextExtraction

def find_best_chunk(collection, request):
    request = TextExtraction.lemmatization_and_punct_clean(request)
    results = collection.query(
        query_texts=[f'{request}'],
        n_results=1
    )
    best_distance = results['distances'][0][0]
    best_chunk = results['documents'][0][0]
    return best_chunk, best_distance

