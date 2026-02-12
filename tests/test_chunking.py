from src.chunk_processing import chunk_text_by_sentence, find_best_chunk
from unittest.mock import Mock, patch


class TestChunkTextBySentence:

    def test_chunk_text_basic(self):
        text = "Hello world. This is a test. Another sentence."
        result = chunk_text_by_sentence(text, 20)
        assert isinstance(result, list)
        assert len(result) > 0


    def test_chunk_text_single_sentence(self):
        text = "Hello world."
        result = chunk_text_by_sentence(text, 50)
        assert result == ["Hello world."]


    def test_chunk_text_multiple_sentences(self):
        text = "First sentence. Second sentence. Third sentence."
        result = chunk_text_by_sentence(text, 20)
        assert len(result) >= 2
        assert all(isinstance(chunk, str) for chunk in result)


    def test_chunk_text_long_text(self):
        text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur tincidunt ipsum at nibh efficitur, ut vehicula lectus eleifend. Pellentesque id libero ipsum. Ut luctus lacus condimentum, semper leo nec, fermentum diam. Suspendisse sit amet diam at ante interdum auctor vitae vitae enim. Vivamus cursus elementum mi laoreet dapibus. Phasellus sed posuere lectus. Maecenas et dui orci. Aenean eu varius velit, et sagittis augue. Pellentesque sollicitudin mollis ipsum, sit amet fermentum odio rhoncus eget.
            Aliquam accumsan sed ante eget rutrum. Nulla molestie ullamcorper dolor, et blandit leo viverra at. Suspendisse sit amet ante quis felis placerat dignissim. Vivamus sagittis, ante ut tincidunt sollicitudin, risus sem lacinia velit, fringilla faucibus eros lectus vel ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque nunc quam, ultrices vel vehicula in, porta sed arcu.
            Nunc vulputate enim sed aliquam tempor. Praesent vel diam faucibus, faucibus turpis vitae, scelerisque turpis. Ut luctus quis massa quis rutrum. Nam viverra mattis elit suscipit consequat. Phasellus erat odio, placerat vitae nunc vulputate, congue rhoncus arcu. Quisque facilisis eros erat, ac venenatis massa sodales eget. Nulla in erat ut neque finibus pretium. Suspendisse nec nunc nec dolor accumsan iaculis a quis nulla. Donec faucibus euismod sapien, a accumsan lectus venenatis eget.
            Praesent elementum, neque et condimentum tempus, nisi lectus pellentesque dui, non commodo tellus purus sit amet sapien. Suspendisse posuere vel tortor ut sagittis. Pellentesque consequat urna lacus. Suspendisse quis tellus et ex convallis pretium. Sed enim leo, blandit ut vestibulum eu, bibendum eget nibh. Aliquam at diam non quam consequat malesuada.
            Nullam sagittis vulputate diam, et efficitur magna luctus eu. Fusce eget libero rhoncus, pellentesque risus non, malesuada nibh. Nam mollis metus urna, sit amet pulvinar ipsum maximus sit amet. Suspendisse potenti. Fusce efficitur eros quis laoreet luctus. In condimentum posuere nibh ut mollis. Morbi nec justo condimentum, elementum dolor ut, eleifend erat.
            Vestibulum posuere justo in pulvinar cursus. Suspendisse ac risus non quam cursus efficitur a in urna. Fusce nulla nulla, laoreet eu lorem id, sagittis viverra augue. Phasellus eu nunc in leo efficitur ullamcorper non eget lectus. Phasellus feugiat diam vitae nibh vulputate efficitur. Donec sit amet euismod nunc, ut malesuada sem. Ut iaculis in ex et suscipit. Aenean ex nunc, facilisis id pretium sit amet, consequat ultricies lacus. Sed volutpat nisl eu lorem vulputate consectetur.
            Suspendisse finibus ante ante, quis maximus ex sodales at. Curabitur porta mauris sed tincidunt egestas. Sed nulla metus, elementum non augue vitae, porttitor commodo diam. Cras ut eros in lorem interdum ultrices vitae at augue. Morbi eu dapibus nisl, quis porta tortor. Aliquam sit amet dui ut orci pretium mattis. Morbi cursus rutrum pulvinar. Donec ut metus nulla. Duis porta vulputate sollicitudin. Sed accumsan vitae turpis a feugiat."""
        result = chunk_text_by_sentence(text, 1000)
        assert len(result) > 0


    def test_chunk_text_preserves_content(self):
        text = "First. Second. Third."
        result = chunk_text_by_sentence(text, 100)
        full_text = " ".join(result)
        assert "First" in full_text and "Second" in full_text and "Third" in full_text


    def test_chunk_text_different_punctuation(self):
        text = "Question? Exclamation! Statement. Another one."
        result = chunk_text_by_sentence(text, 10)
        assert len(result) >= 4


    def test_chunk_text_empty_string(self):
        text = ""
        result = chunk_text_by_sentence(text, 20)
        assert result == [""]


    def test_chunk_text_single_word(self):
        text = "Word"
        result = chunk_text_by_sentence(text, 10)
        assert result == ["Word"]


    def test_chunk_text_abbreviations(self):
        text = "Dr. Smith is here. He will meet you at noon."
        result = chunk_text_by_sentence(text, 10)
        assert len(result) > 0
        assert any("Dr. Smith is here." in chunk for chunk in result)


class TestFindBestChunk:

    def test_find_best_chunk_basic(self):
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'distances': [[0.5]],
            'documents': [['This is the best chunk']]
        }
        
        with patch('src.chunk_processing.TextExtraction.lemmatization_and_punct_clean', return_value='test query'):
            chunk, distance = find_best_chunk(mock_collection, 'test query')
        
        assert chunk == 'This is the best chunk'
        assert distance == 0.5

    def test_find_best_chunk_calls_query_once(self):
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'distances': [[0.1]],
            'documents': [['chunk']]
        }
        
        with patch('src.chunk_processing.TextExtraction.lemmatization_and_punct_clean', return_value='request'):
            find_best_chunk(mock_collection, 'request')
        
        mock_collection.query.assert_called_once_with(query_texts=['request'], n_results=1)

    def test_find_best_chunk_zero_distance(self):
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'distances': [[0.0]],
            'documents': [['Perfect match']]
        }
        
        with patch('src.chunk_processing.TextExtraction.lemmatization_and_punct_clean', return_value='perfect'):
            chunk, distance = find_best_chunk(mock_collection, 'perfect')
        
        assert distance == 0.0
        assert chunk == 'Perfect match'

    def test_find_best_chunk_high_distance(self):
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'distances': [[0.95]],
            'documents': [['Poor match']]
        }
        
        with patch('src.chunk_processing.TextExtraction.lemmatization_and_punct_clean', return_value='query'):
            chunk, distance = find_best_chunk(mock_collection, 'query')
        
        assert distance == 0.95

    def test_find_best_chunk_returns_tuple(self):
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'distances': [[0.3]],
            'documents': [['Some text']]
        }
        
        with patch('src.chunk_processing.TextExtraction.lemmatization_and_punct_clean', return_value='text'):
            result = find_best_chunk(mock_collection, 'text')
        
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_find_best_chunk_lemmatization_called(self):
        mock_collection = Mock()
        mock_collection.query.return_value = {
            'distances': [[0.2]],
            'documents': [['cleaned chunk']]
        }
        
        with patch('src.chunk_processing.TextExtraction.lemmatization_and_punct_clean', return_value='cleaned') as mock_lem:
            find_best_chunk(mock_collection, 'original request')
            mock_lem.assert_called_once_with('original request')

    def test_find_best_chunk_long_text(self):
        mock_collection = Mock()
        long_chunk = 'This is a very long chunk ' * 20
        mock_collection.query.return_value = {
            'distances': [[0.4]],
            'documents': [[long_chunk]]
        }
        
        with patch('src.chunk_processing.TextExtraction.lemmatization_and_punct_clean', return_value='long'):
            chunk, distance = find_best_chunk(mock_collection, 'long query')
        
        assert chunk == long_chunk
        assert distance == 0.4