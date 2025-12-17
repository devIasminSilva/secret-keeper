import flet as ft
from ui.styles import AppTextStyles, AppColors
from ui.components import PrimaryButton

def main_menu_view(page: ft.Page):
    def go_encrypt(e):
        page.go("/encrypt")

    def go_decrypt(e):
        page.go("/decrypt")

    title = ft.Text("SECRET KEEPER", style=AppTextStyles.TITLE)
    subtitle = ft.Text("Privacy, Simplified.", style=AppTextStyles.SUBTITLE)
    
    encrypt_btn = PrimaryButton(text="Encrypt", on_click=go_encrypt, width=150)
    decrypt_btn = PrimaryButton(text="Decrypt", on_click=go_decrypt, width=150)

    buttons = ft.Row(
        controls=[encrypt_btn, decrypt_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=20
    )

    content = ft.Column(
        controls=[
            ft.Container(height=50),
            title,
            subtitle,
            ft.Container(height=80),
            buttons
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.View(
        "/",
        controls=[
             ft.Container(
                content=content,
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        bgcolor=AppColors.BACKGROUND,
        padding=0
    )
