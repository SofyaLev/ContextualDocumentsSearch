import chromadb

def Create_collection(text_chunks, docname):
    client = chromadb.Client()
    collection = client.get_or_create_collection(name=docname)
    collection.add(
    documents=text_chunks,
    ids=[f'{x}' for x in range(len(text_chunks))])
    return collection