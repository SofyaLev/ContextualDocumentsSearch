import flet

def create_main_layout(on_search_click):
    search_input = flet.TextField(
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
                    search_input,
                    flet.IconButton(flet.Icons.SEARCH, on_click=on_search_click)
                ]
            ),
            flet.Text("Found fragments:", size=20, weight=flet.FontWeight.BOLD),
            results_list,
        ],
        expand = True
    )

    return content, search_input, results_list