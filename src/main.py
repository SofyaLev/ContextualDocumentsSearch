import flet
from ui.layout import create_main_layout

def main(page: flet.Page):
    page.title = "Contextual Documents Search App"
    page.window_width = page.width
    page.window_height = page.height

    def handle_search(e):
        if search_field.value:
            results_area.controls.append(flet.Text(f"Looking for: {search_field.value}..."))
            page.update()

    layout, search_field, results_area = create_main_layout(handle_search)

    page.add(layout)

if __name__ == "__main__":
    flet.app(target=main)
