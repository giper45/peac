import flet as ft
from peac.gui.ui.app import PeacFletApp


def start_flet_gui():
    def main(page: ft.Page):
        PeacFletApp(page)

    ft.app(target=main)


if __name__ == "__main__":
    start_flet_gui()
