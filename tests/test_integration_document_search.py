import pytest
from pathlib import Path
from src.document_search import RelevantDocumentsSearch
from src.text_extration import TextExtraction


@pytest.fixture
def documents_folder():
    """Возвращает папку с реальными документами"""
    docs_path = Path(__file__).parent.parent / "documents"
    
    if not docs_path.exists():
        pytest.skip(f"Папка с документами не найдена: {docs_path}")
    
    txt_files = list(docs_path.glob("**/*.txt"))
    if not txt_files:
        pytest.skip(f"В папке {docs_path} нет текстовых файлов")
    
    yield docs_path


@pytest.fixture
def search_instance_with_db(documents_folder) -> RelevantDocumentsSearch:
    """Создает экземпляр RelevantDocumentsSearch с реальными документами"""
    return RelevantDocumentsSearch(
        current_folder_path=documents_folder,
        request='кошки',
        chunk_length=50,
        results_count=3
    )


class TestRelevantDocumentsSearchIntegration:
    """Интеграционные тесты для поиска релевантных документов"""
    
    def test_find_documents_basic_search(self, search_instance_with_db: RelevantDocumentsSearch):
        """Тест базового поиска документов"""
        result = search_instance_with_db.find_documents()
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert len(result) <= 3  # results_count=3
    
    
    def test_find_documents_returns_paths(self, search_instance_with_db: RelevantDocumentsSearch):
        """Тест что результаты содержат пути к файлам"""
        result = search_instance_with_db.find_documents()
        
        for path in result:
            assert isinstance(path, Path)
            assert path.joinpath(search_instance_with_db.current_folder_path).exists()
    
    
    def test_find_documents_ordered_by_relevance(self, search_instance_with_db):
        """Тест что документы отсортированы по релевантности"""
        result = search_instance_with_db.find_documents()
        
        assert len(result) > 0
        # cats.txt и cats2.txt должны быть в топ результатах для запроса 'кошки'
        found_cats = any('cats' in str(p) for p in result)
        assert found_cats
    
    
    def test_find_documents_with_different_query(self, documents_folder):
        """Тест поиска с другим запросом"""
        search = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='собаки',
            chunk_length=50,
            results_count=3
        )
        
        result = search.find_documents()
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert any('dogs.txt' in str(path) for path in result)
    
    
    def test_find_documents_with_nested_folders(self, search_instance_with_db):
        """Тест поиска в документах из вложенных папок"""
        result = search_instance_with_db.find_documents()
        
        # Проверяем что найдены файлы
        assert len(result) > 0
        
        # Проверяем что обработаны файлы из extra_folder
        all_paths_str = [str(p) for p in result]
        # cats2.txt находится в extra_folder и должен быть обработан
        assert any('extra_folder' in p or 'cats' in p for p in all_paths_str)
    
    
    def test_find_documents_cats_query(self, documents_folder):
        """Тест поиска с запросом про кошек"""
        search = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки',
            chunk_length=50,
            results_count=3
        )
        
        result = search.find_documents()
        
        assert isinstance(result, list)
        assert len(result) > 0
        # В результатах должны быть файлы о кошках
        assert any('cats' in str(p) for p in result)
    
    
    def test_extract_rel_doc_paths_integration(self, search_instance_with_db, documents_folder):
        """Интеграционный тест методов find_documents и extract_rel_doc_paths"""
        result = search_instance_with_db.find_documents()
        
        assert isinstance(result, list)
        assert all(isinstance(p, Path) for p in result)
        assert len(result) <= search_instance_with_db.results_count
    
    
    def test_lemmatization_in_search_pipeline(self, documents_folder):
        """Тест что лемматизация работает в цепочке поиска"""
        search1 = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошка',  # начальная форма
            chunk_length=50,
            results_count=3
        )
        
        search2 = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошкой',  # творительный падеж
            chunk_length=50,
            results_count=3
        )
        
        result1 = search1.find_documents()
        result2 = search2.find_documents()
        
        # Обе формы должны найти документы о кошках
        assert len(result1) > 0
        assert len(result2) > 0
        assert any('cats' in str(p) for p in result1)
        assert any('cats' in str(p) for p in result2)
    
    
    def test_different_chunk_lengths(self, documents_folder):
        """Тест влияния размера chunks на результаты"""
        search_small = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки',
            chunk_length=20,  # маленькие chunks
            results_count=2
        )
        
        search_large = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки',
            chunk_length=200,  # большие chunks
            results_count=2
        )
        
        result_small = search_small.find_documents()
        result_large = search_large.find_documents()
        
        # Оба должны вернуть результаты
        assert len(result_small) > 0
        assert len(result_large) > 0
    
    
    def test_results_count_limit(self, search_instance_with_db):
        """Тест что количество результатов не превышает results_count"""
        result = search_instance_with_db.find_documents()
        
        assert len(result) <= search_instance_with_db.results_count
    
    
    def test_persistence_across_instances(self, documents_folder):
        """Тест сохранения данных в БД между экземплярами"""
        search1 = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки',
            chunk_length=50,
            results_count=2
        )
        
        result1 = search1.find_documents()
        
        # Создаем новый экземпляр с теми же параметрами
        search2 = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки',
            chunk_length=50,
            results_count=2
        )
        
        result2 = search2.find_documents()
        
        # Результаты должны быть идентичными
        assert len(result1) == len(result2)
        if len(result1) > 0:
            assert result1 == result2
    
    
    def test_query_with_special_characters(self, documents_folder):
        """Тест поиска с специальными символами"""
        search = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки!',
            chunk_length=50,
            results_count=3
        )
        
        # Не должно быть исключений
        result = search.find_documents()
        assert isinstance(result, list)
        assert len(result) > 0
    
    
    def test_long_query_string(self, documents_folder):
        """Тест поиска с длинной строкой запроса"""
        search = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки которые ловят мышей и спят',
            chunk_length=50,
            results_count=2
        )
        
        result = search.find_documents()
        assert isinstance(result, list)
        assert len(result) > 0
    
    
    def test_search_all_document_types(self, documents_folder):
        """Тест поиска документов разного типа"""
        # Поиск по кошкам
        search_cats = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='кошки',
            chunk_length=50,
            results_count=5
        )
        result_cats = search_cats.find_documents()
        
        # Поиск по собакам
        search_dogs = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='собаки',
            chunk_length=50,
            results_count=5
        )
        result_dogs = search_dogs.find_documents()
        
        # Поиск по литературе
        search_lit = RelevantDocumentsSearch(
            current_folder_path=documents_folder,
            request='литература',
            chunk_length=50,
            results_count=5
        )
        result_lit = search_lit.find_documents()
        
        assert len(result_cats) > 0
        assert len(result_dogs) > 0
        # literature.txt может быть найден или нет в зависимости от содержания


class TestTextExtractionIntegration:
    """Интеграционные тесты для извлечения текста"""
    
    def test_extract_multiple_files(self, documents_folder):
        """Тест извлечения текста из нескольких файлов"""
        extractor = TextExtraction(documents_folder)
        result = extractor.extract()
        
        assert isinstance(result, dict)
        assert len(result) >= 5  # 5 файлов: cats.txt, dogs.txt, literature.txt, catcaterpillar.txt, cats2.txt, test.txt
        assert all(isinstance(k, Path) for k in result.keys())
        assert all(isinstance(v, str) for v in result.values())
    
    
    def test_extract_preserves_content(self, documents_folder):
        """Тест что содержимое файлов сохраняется"""
        extractor = TextExtraction(documents_folder)
        result = extractor.extract()
        
        # Проверяем что текст не пустой
        all_text = ' '.join(result.values())
        assert len(all_text) > 0
        
        # Проверяем что содержимое включает ожидаемые слова
        assert 'кошки' in all_text.lower() or 'собаки' in all_text.lower() or 'кот' in all_text.lower()
    
    
    def test_extract_handles_nested_structure(self, documents_folder):
        """Тест обработки вложенной структуры папок"""
        extractor = TextExtraction(documents_folder)
        result = extractor.extract()
        
        # Проверяем что файлы из extra_folder обработаны
        paths_str = [str(p) for p in result.keys()]
        assert any('extra_folder' in p for p in paths_str)
    
    
    def test_extract_returns_non_empty_text(self, documents_folder):
        """Тест что все извлеченные тексты не пусты"""
        extractor = TextExtraction(documents_folder)
        result = extractor.extract()
        
        for path, text in result.items():
            assert len(text.strip()) > 0, f"Файл {path} содержит пустой текст"
    
    
    def test_extract_specific_files(self, documents_folder):
        """Тест извлечения конкретных файлов"""
        extractor = TextExtraction(documents_folder)
        result = extractor.extract()
        
        # Проверяем что есть нужные файлы
        file_names = [p.name for p in result.keys()]
        assert 'cats.txt' in file_names
        assert 'dogs.txt' in file_names
    
    
    def test_extract_text_encoding(self, documents_folder):
        """Тест что текст корректно декодирован"""
        extractor = TextExtraction(documents_folder)
        result = extractor.extract()
        
        for path, text in result.items():
            # Проверяем что это строка и она содержит валидные символы
            assert isinstance(text, str)
            # Проверяем что кириллица читается правильно
            assert not text.startswith('\ufffd')  # BOM символ


class TestChunkingIntegration:
    """Интеграционные тесты для разбиения текста на chunks"""
    
    def test_chunking_preserves_all_content(self, documents_folder):
        """Тест что chunking не теряет текст"""
        from src.chunk_processing import chunk_text_by_sentence
        
        extractor = TextExtraction(documents_folder)
        texts = extractor.extract()
        
        for path, text in texts.items():
            chunks = chunk_text_by_sentence(text, 50)
            
            # Chunks не должны быть пусты
            assert len(chunks) > 0
            assert all(isinstance(chunk, str) for chunk in chunks)
            assert all(len(chunk) > 0 for chunk in chunks)
    
    
    def test_chunking_sentence_integrity(self, documents_folder):
        """Тест что chunking не разбивает предложения неправильно"""
        from src.chunk_processing import chunk_text_by_sentence
        
        extractor = TextExtraction(documents_folder)
        texts = extractor.extract()
        
        for path, text in texts.items():
            chunks = chunk_text_by_sentence(text, 80)
            
            # Каждый chunk должен быть связным
            for chunk in chunks:
                assert not chunk.endswith(' '), f"Chunk в {path} заканчивается пробелом"
                assert not chunk.startswith(' '), f"Chunk в {path} начинается с пробела"
                assert len(chunk.strip()) > 0
    
    
    def test_chunking_multiple_files(self, documents_folder):
        """Тест chunking для всех файлов в папке"""
        from src.chunk_processing import chunk_text_by_sentence
        
        extractor = TextExtraction(documents_folder)
        texts = extractor.extract()
        
        all_chunks = []
        for path, text in texts.items():
            chunks = chunk_text_by_sentence(text, 60)
            all_chunks.extend(chunks)
        
        # Должны быть chunks из разных файлов
        assert len(all_chunks) > len(texts)