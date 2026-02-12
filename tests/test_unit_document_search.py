import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from src.document_search import RelevantDocumentsSearch

@pytest.fixture
def mock_chroma_client():
    with patch('src.document_search.chromadb.PersistentClient') as mock:
        yield mock


@pytest.fixture
def search_instance(mock_chroma_client):
    return RelevantDocumentsSearch(
        current_folder_path='/test/folder',
        request='test query',
        chunk_length=400,
        results_count=5
    )


class TestRelevantDocumentsSearch:
    
    def test_init(self, search_instance):
        assert search_instance.request == 'test query'
        assert search_instance.current_folder_path == '/test/folder'
        assert search_instance.chunk_length == 400
        assert search_instance.results_count == 5
    
    def test_create_collection(self, search_instance):
        mock_collection = MagicMock()
        search_instance.client.get_or_create_collection.return_value = mock_collection
        
        with patch('src.document_search.TextExtraction.lemmatization_and_punct_clean', return_value='cleaned'):
            chunks = ['chunk1', 'chunk2']
            result = search_instance.create_collection(chunks, '/path/to/doc.txt')
        
        assert result == mock_collection
        search_instance.client.get_or_create_collection.assert_called_once()
        mock_collection.upsert.assert_called_once()
    
    def test_extract_rel_doc_paths(self, search_instance):
        distances = {'/doc1.txt': 0.5, '/doc2.txt': 0.3, '/doc3.txt': 0.7}
        result = search_instance.extract_rel_doc_paths(distances)
        
        assert len(result) == 3
        assert result[0] == '/doc2.txt'
        assert result[1] == '/doc1.txt'
    
    def test_extract_rel_doc_paths_limit_results(self, search_instance):
        distances = {f'/doc{i}.txt': i * 0.1 for i in range(10)}
        result = search_instance.extract_rel_doc_paths(distances)
        
        assert len(result) == 5
    
    @patch('src.document_search.TextExtraction')
    @patch('src.document_search.chunk_text_by_sentence')
    @patch('src.document_search.find_best_chunk')
    def test_find_documents(self, mock_find_chunk, mock_chunk_text, mock_text_ext, search_instance):
        mock_text_ext.return_value.extract.return_value = {'/doc1.txt': 'text1', '/doc2.txt': 'text2'}
        mock_chunk_text.return_value = ['chunk1', 'chunk2']
        mock_find_chunk.return_value = ('best_chunk', 0.5)
        
        search_instance.client.get_or_create_collection.return_value = MagicMock()
        
        with patch.object(search_instance, 'extract_rel_doc_paths', return_value=['/doc1.txt']):
            result = search_instance.find_documents()
        
        assert result == ['/doc1.txt']