import flet as ft
import os
from ui.styles import AppFonts, AppColors
from ui.views.main_menu import main_menu_view
from ui.views.encrypt_view import encrypt_view
from ui.views.decrypt_view import decrypt_view

def main(page: ft.Page):

    page.title = "Secret Keeper"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 800
    page.window.height = 500
    page.window.resizable = False
    icon_path = os.path.abspath(os.path.join("assets", "icon.ico"))
    page.window.icon = icon_path

    page.fonts = {
        "Space Grotesk": "https://fonts.gstatic.com/s/spacegrotesk/v13/V8mQoQDjQSkFtoMM3T6r8E7mF71Q-gOoraIAEj4o.woff2",
        "Roboto": "https://fonts.gstatic.com/s/roboto/v20/KFOmCnqEu92Fr1Mu4mxK.woff2"
    }
    
    page.theme = ft.Theme(
        font_family=AppFonts.body_font,
        color_scheme=ft.ColorScheme(
            background=AppColors.BACKGROUND,
            surface=AppColors.SURFACE,
            primary=AppColors.ACCENT
        )
    )

    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            page.views.append(main_menu_view(page))
        if page.route == "/encrypt":
            page.views.append(encrypt_view(page))
        elif page.route == "/decrypt":
            page.views.append(decrypt_view(page))
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/")

if __name__ == "__main__":
    ft.app(target=main)
