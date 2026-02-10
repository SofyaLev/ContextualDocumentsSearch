import flet
import os
from ui.layout import create_main_layout

def main(page: flet.Page):
    """Точка входа в приложение и управление состояниями.
    Настраивает логику взаимодействия пользователя с интерфейсом и вызывает
    обновление визуальных компонентов.

    page (flet.Page): Главное окно приложения.
    """

    page.title = "Contextual Documents Search App"
    page.window_width = page.width
    page.window_height = page.height

    def handle_folder_result(e: flet.FilePickerResultEvent):
        """Обработать результат выбора директории пользователем.
        Обновляет текстовую метку на главном экране при успешном выборе.

        e (flet.FilePickerResultEvent): Объект события с путем к папке.
        """

        if e.path:
            selected_path_label.value = f"Selected: {e.path}"
            print(f"Directory selected: {e.path}")
            page.update()

    def update_results(file_paths):
        """Отобразить найденные файлы в списке в заданном порядке.
        Очищает предыдущие результаты и создает интерактивные карточки для новых путей.

        file_paths (list[str]): Массив строк с абсолютными путями к файлам.

        Пример:
            >>> update_results(['C:/file1.pdf', 'C:/file2.docx'])
        """

        results_area.controls.clear()

        if not file_paths:
            results_area.controls.append(flet.Text("No files found", color=flet.Colors.RED_400))
        else:
            for path in file_paths:
                file_name = os.path.basename(path)
                results_area.controls.append(
                    flet.Card(
                        content=flet.Container(
                            content=flet.ListTile(
                                leading=flet.Icon(flet.Icons.INSERT_DRIVE_FILE, color=flet.Colors.BLUE_400),
                                title=flet.Text(file_name, weight=flet.FontWeight.BOLD),
                                subtitle=flet.Text(path, size=12),
                                on_click=lambda _, p=path: print(f"Selected file: {p}")
                            ),
                            padding=5
                        )
                    )
                )
        page.update()

    def handle_search(e):
        """Запустить процесс поиска и визуализировать состояние загрузки.
        Управляет видимостью ProgressBar и передает данные для отрисовки.

        e (any): Событие нажатия кнопки или клавиши Enter.
        """

        if search_field.value:
            loader.visible = True
            results_area.controls.clear()
            page.update()

            # имитация получения данных - сделать вызов бекенда
            mock_results = [
                "C:/mock_data/cats.txt",
                "C:/mock_data/dogs.docx",
                "C:/mock_data/catcaterpillar.pdf",
            ]

            loader.visible = False
            update_results(mock_results)

    layout, search_field, results_area, selected_path_label, loader = create_main_layout(page, handle_search, handle_folder_result)

    page.add(layout)

if __name__ == "__main__":
    flet.app(target=main)
