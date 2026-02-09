import flet

def create_main_layout(page: flet.Page, on_search_click, on_folder_result):
    """
    макет с функционалом выбора папки
    """

    directory_picker = flet.FilePicker(on_result=on_folder_result)
    page.overlay.append(directory_picker)

    path_display = flet.Text("No folder selected", italic=True, color=flet.colors.GREY_500)

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
                        icon = flet.icons.FOLDER_OPEN,
                        on_click = lambda _: directory_picker.get_directory_path(),
                    ),
                    path_display
                ]
            ),

            flet.Row(
                [
                    search_input,
                    flet.IconButton(icon=flet.icons.SEARCH, on_click=on_search_click)
                ]
            ),
            flet.Divider(),
            flet.Text("Found fragments:", size=20, weight=flet.FontWeight.BOLD),
            results_list
        ],
        expand = True,
        spacing = 15
    )

    return content, search_input, results_list, path_display
