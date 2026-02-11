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

    def show_message(text, color=flet.Colors.BLUE_400):
        """Отобразить всплывающее уведомление пользователю.
        Используется для информирования об ошибках или действиях.

        text (str): Текст сообщения.
        color (flet.Colors): Цвет фона уведомления.
        """

        # В новых версиях Flet это самый надежный способ:
        snack = flet.SnackBar(
            content=flet.Text(text),
            bgcolor=color,
            action="OK"  # Добавим кнопку, чтобы уведомление не исчезало само сразу
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def handle_folder_result(e: flet.FilePickerResultEvent):
        """Обработать результат выбора директории пользователем.
        Обновляет текстовую метку на главном экране при успешном выборе.

        e (flet.FilePickerResultEvent): Объект события с путем к папке.
        """

        if e.path:
            selected_path_label.value = f"Selected: {e.path}"
            show_message(f"Directory selected: {os.path.basename(e.path)}")

    def handle_clear(e):
        """Очистить область результатов и поле поиска.
        Сбрасывает визуальное состояние списка найденных фрагментов.
        """

        results_area.controls.clear()
        search_field.value = ""
        show_message("Results cleared", color=flet.Colors.GREY_700)

    def update_results(file_paths):
        """Отобразить найденные файлы в списке в заданном порядке.
        Очищает предыдущие результаты и создает интерактивные карточки для новых путей.

        file_paths (list[str]): Массив строк с абсолютными путями к файлам.

        Пример:
            >>> update_results(['C:/file1.pdf', 'C:/file2.docx'])
        """

        results_area.controls.clear()

        if not file_paths:
            show_message("No matches found", color=flet.Colors.ORANGE_700)
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
                                on_click=lambda _, p=path: show_message(f"Opening {os.path.basename(p)}...")
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

        if not search_field.value:
            show_message("Please enter a search term", color=flet.Colors.RED_400)
            return

        loader.visible = True
        page.update()

        # имитация получения данных - сделать вызов бекенда
        mock_results = [
            "C:/mock_data/cats.txt",
            "C:/mock_data/catcaterpillar.pdf",
        ] if "cat" in search_field.value else []

        loader.visible = False
        update_results(mock_results)

    layout, search_field, results_area, selected_path_label, loader = create_main_layout(page, handle_search, handle_folder_result, handle_clear)

    page.add(layout)

if __name__ == "__main__":
    flet.app(target=main)
