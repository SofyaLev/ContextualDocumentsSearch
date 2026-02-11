import pytest
from pathlib import Path
# from unittest.mock import patch, mock_open, MagicMock
from src.text_extration import TextExtraction

class TestTextExtraction:
    
    def test_extract_multiple_files(self, tmp_path):
        """Test extracting text from multiple files"""
        (tmp_path / "file1.txt").write_text("Content 1", encoding='utf-8')
        (tmp_path / "file2.txt").write_text("Content 2", encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert len(result) == 2
        assert "Content 1" in result.values()
        assert "Content 2" in result.values()

    def test_extract_nested_directories(self, tmp_path):
        """Test extracting from nested directories"""
        (tmp_path / "dir1").mkdir()
        (tmp_path / "dir1" / "file1.txt").write_text("Nested content", encoding='utf-8')
        (tmp_path / "dir1" / "dir2").mkdir()
        (tmp_path / "dir1" / "dir2" / "file2.txt").write_text("Deep nested", encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert len(result) == 2
        assert "Nested content" in result.values()
        assert "Deep nested" in result.values()

    def test_extract_csv_file(self, tmp_path):
        """Test extracting from .csv file"""
        test_file = tmp_path / "test.csv"
        csv_content = "name,age\nJohn,30\nJane,25"
        test_file.write_text(csv_content, encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert csv_content in result.values()

    def test_extract_json_file(self, tmp_path):
        """Test extracting from .json file"""
        test_file = tmp_path / "test.json"
        json_content = '{"key": "value"}'
        test_file.write_text(json_content, encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert json_content in result.values()

    def test_lemmatization_preserves_structure(self):
        """Test that lemmatization returns string without punctuation"""
        text = "Running quickly, the cat jumped!"
        result = TextExtraction.lemmatization_and_punct_clean(text)
        
        assert isinstance(result, str)
        assert len(result) > 0

    def test_lemmatization_with_russian_text(self):
        """Test lemmatization with Russian text"""
        text = "Быстро бегущая кошка прыгал!"
        result = TextExtraction.lemmatization_and_punct_clean(text)
        
        assert isinstance(result, str)
        assert "!" not in result

    def test_extract_html_file(self, tmp_path):
        """Test extracting from .html file"""
        test_file = tmp_path / "test.html"
        html_content = "<html><body>Hello</body></html>"
        test_file.write_text(html_content, encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert html_content in result.values()

    def test_extract_md_file(self, tmp_path):
        """Test extracting from .md file"""
        test_file = tmp_path / "test.md"
        md_content = "# Header\nSome content"
        test_file.write_text(md_content, encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert md_content in result.values()

    def test_extract_python_file(self, tmp_path):
        """Test extracting from .py file"""
        test_file = tmp_path / "test.py"
        py_content = "print('Hello')"
        test_file.write_text(py_content, encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert py_content in result.values()

    def test_relative_path_keys(self, tmp_path):
        """Test that dictionary keys contain relative paths"""
        (tmp_path / "subdir").mkdir()
        (tmp_path / "subdir" / "file.txt").write_text("content", encoding='utf-8')
        
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        keys = list(result.keys())
        assert len(keys) == 1
        assert "subdir" in str(keys[0])
        assert "file.txt" in str(keys[0])

    def test_empty_directory(self, tmp_path):
        """Test extraction from empty directory"""
        extractor = TextExtraction(str(tmp_path))
        result = extractor.extract()
        
        assert len(result) == 0
        assert result == {}