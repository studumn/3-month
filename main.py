import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Моё первое приложение"
    page.scroll = "adaptive"
    page.window_width = 400
    page.window_height = 400
    page.window_resizable = False

    greeting_text = ft.Text(size=20)
    name_field = ft.TextField(label="Введите ваше имя", width=300)
    history_list = ft.Column()

    def get_greeting(name):
        hour = datetime.now().hour
        if 6 <= hour < 12:
            return f"Доброе утро, {name}!"
        elif 12 <= hour < 18:
            return f"Добрый день, {name}!"
        elif 18 <= hour < 24:
            return f"Добрый вечер, {name}!"
        else:
            return f"Доброй ночи, {name}!"

    def say_hello(e=None):
        name = name_field.value.strip()
        if name:
            greeting = get_greeting(name)
            greeting_text.value = greeting
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_list.controls.append(ft.Text(f"{now}: {name}"))
            page.update()

    def clear_history(e):
        history_list.controls.clear()
        page.update()

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            theme_icon_button.icon = ft.Icons.DARK_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_icon_button.icon = ft.Icons.LIGHT_MODE
        page.update()


    theme_icon_button = ft.IconButton(
    icon=ft.Icons.LIGHT_MODE,
    tooltip="Переключить тему",
    on_click=toggle_theme
)

    def on_startup(e):
        say_hello()

    page.add(
        greeting_text,
        name_field,
        ft.Row([
            ft.ElevatedButton("Поздороваться снова", on_click=say_hello),
            ft.IconButton(icon=ft.Icons.DELETE, tooltip="Очистить историю", on_click=clear_history),
            theme_icon_button,
        ]),
        ft.Text("История приветствий:"),
        history_list
    )

    page.on_connect = on_startup

ft.app(target=main, view=ft.AppView.FLET_APP)
