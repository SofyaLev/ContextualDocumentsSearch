from pathlib import Path
import docx2txt
import PyPDF2
from nltk import word_tokenize, SnowballStemmer
from nltk.stem import WordNetLemmatizer
import re


class TextExtraction:

    def __init__(self, main_folder_path):
        """ Конструктор класса для извлечения текста
        args:
            main_folder_path: путь до папки, в которой пользователь планирует искать файлы
        returns:
        """
        self.main_folder_path = main_folder_path
        self.full_paths = []
        self.texts = {}

    def extract(self) -> dict:
        """ Метод для извлечения текста из всех найденных файлов
        args:
        returns:
            texts(dict): словарь вида { <путь>: 'текст файла' }
        """
        self.get_paths(self.main_folder_path)
        for path in self.full_paths:
            self.read_text_from_file(path)
        return self.texts.copy()

    def get_paths(self, folder_path) -> None:
        """ Метод для поиска путей всех файлов """
        for path in Path.iterdir(Path(folder_path)):
            if Path.is_dir(path):
                self.get_paths(path)
            else:
                self.full_paths.append(path)

    @staticmethod
    def lemmatization_and_punct_clean(text):
        """ Метод для лемматизации текста и удаления знаков препинания.
        Лемматизация текста - удаление окончаний для повышения эффективности обработки"""
        en_lemmatizer = WordNetLemmatizer()
        ru_stemmer = SnowballStemmer("russian")
        lemmatized_words = []
        tokens = word_tokenize(text)
        for token in tokens:
            if re.search(r'[а-яёА-ЯЁ]', token):
                lemmatized_words.append(ru_stemmer.stem(token))
            else:
                lemmatized_words.append(en_lemmatizer.lemmatize(token))
        lemmed = ' '.join(lemmatized_words)
        text = re.sub(r'[^\w\s]', '', lemmed)
        return text

    def read_text_from_file(self, path: Path):
        """ Функция для извлечения текста из файлов разного расширения"""
        extension = path.suffix
        relative_path = path.relative_to(self.main_folder_path)
        file_text = ""
        if extension in ('.txt', '.csv', '.json', '.xml', '.html', '.md', '.log', '.py'):
            with open(path, 'r', encoding='utf-8') as file:
                file_text = file.read()

        elif extension in ('.doc', '.docx'):
            file_text = docx2txt.process(path)

        elif extension == '.pdf':
            with open(path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    file_text += page.extract_text()
        else:
            pass
        self.texts[relative_path] = file_text
