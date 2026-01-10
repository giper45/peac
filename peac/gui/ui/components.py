import flet as ft


def section_header(title: str, subtitle: str, on_add):
    return ft.Row(
        [
            ft.Column(
                [
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(subtitle, size=12, color=ft.colors.GREY_700),
                ],
                expand=True,
                spacing=2,
            ),
            ft.FilledButton("Add", icon=ft.icons.ADD, on_click=lambda _: on_add()),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )
