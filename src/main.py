import flet
from ui.layout import create_main_layout

def main(page: flet.Page):
    page.title = "Contextual Documents Search App"
    page.window_width = page.width
    page.window_height = page.height

    def handle_folder_result(e: flet.FilePickerResultEvent):
        if e.path:
            selected_path_label.value = f"Selected: {e.path}"
            print(f"Directory selected: {e.path}")
            page.update()

    def handle_search(e):
        if search_field.value:
            results_area.controls.append(flet.Text(f"Searching for: {search_field.value}..."))
            page.update()

    layout, search_field, results_area, selected_path_label = create_main_layout(page, handle_search, handle_folder_result)

    page.add(layout)

if __name__ == "__main__":
    flet.app(target=main)
