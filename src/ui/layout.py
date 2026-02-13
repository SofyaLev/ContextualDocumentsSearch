import flet

def create_main_layout(page: flet.Page, on_search_click, on_folder_result, on_clear_click):
    """Создать базовый шаблон интерфейса приложения.
    Функция инициализирует основные визуальные компоненты, включая поле поиска,
    список результатов и индикатор загрузки.

    page (flet.Page): Объект страницы приложения для регистрации overlay.
    on_search_click (function): Обработчик события запуска поиска.
    on_folder_result (function): Обработчик события выбора папки.
    on_clear_click (function): Обработчик для очистки списка результатов.
    """

    directory_picker = flet.FilePicker(on_result=on_folder_result)
    page.overlay.append(directory_picker)

    path_display = flet.Text("No folder selected", italic=True, color=flet.Colors.GREY_500)

    loader = flet.ProgressBar(visible=False, color=flet.Colors.BLUE_700)

    search_input = flet.TextField(
        label="Search term",
        hint_text="Enter search term",
        expand = True,
        on_submit = on_search_click,
    )

    results_list = flet.ListView(
        expand = True,
        spacing = 10,
        padding = 20,
    )

    content = flet.Column(
        [
            flet.Row(
                [
                    flet.ElevatedButton(
                        "Select a folder to search",
                        icon = flet.Icons.FOLDER_OPEN,
                        on_click = lambda _: directory_picker.get_directory_path(),
                    ),
                    path_display
                ]
            ),

            flet.Row(
                [
                    search_input,
                    flet.IconButton(icon=flet.Icons.SEARCH, on_click=on_search_click),
                    flet.IconButton(
                        icon=flet.Icons.DELETE_OUTLINED,
                        on_click=on_clear_click,
                        tooltip="Clear search results"
                    )
                ]
            ),
            loader,
            flet.Divider(),
            flet.Text("Found fragments:", size=20, weight=flet.FontWeight.BOLD),
            results_list
        ],
        expand = True,
        spacing = 15
    )

    return content, search_input, results_list, path_display, loader
