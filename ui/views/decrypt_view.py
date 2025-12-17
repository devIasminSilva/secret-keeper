import flet as ft
import threading
from ui.styles import AppColors
from ui.components import PrimaryButton, InputField, MinimalContainer, show_dialog
from core.crypto import CryptoService

def decrypt_view(page: ft.Page):
    file_input = InputField(
        hint_text="Select file (.enc)", 
        icon="description", 
        read_only=True
    )
    
    password_input = InputField(
        hint_text="Password", 
        icon="lock", 
        password=True, 
        can_reveal_password=True
    )

    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:
            file_input.value = e.files[0].path
            file_input.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)


    def select_file(e):
        file_picker.pick_files(allow_multiple=False, allowed_extensions=["enc"])

    file_container = ft.Stack(
        controls=[
            MinimalContainer(file_input),
            ft.Container(
                on_click=select_file,
                bgcolor=ft.Colors.TRANSPARENT,
                height=50,
                width=500,
            )
        ]
    )
    
    password_container = MinimalContainer(password_input)

    def go_back(e):
        page.go("/")

    def start_decryption(e):
        path = file_input.value
        pwd = password_input.value
        
        if not path or not pwd:
            show_dialog(page, "Error", "Please select a file and enter a password", is_error=True)
            return

        confirm_btn.text = "Decrypting..."
        confirm_btn.disabled = True
        confirm_btn.update()

        def process():
            try:
                CryptoService.decrypt_file(path, pwd)
                show_dialog(page, "Success", "File decrypted successfully!", is_error=False)
            except Exception as ex:
                 show_dialog(page, "Error", f"Decryption failed: {str(ex)}", is_error=True)
            finally:
                confirm_btn.text = "Confirm"
                confirm_btn.disabled = False
                page.update()

        threading.Thread(target=process).start()

    back_btn = PrimaryButton(text="Back", icon="arrow_back", on_click=go_back, width=120)
    confirm_btn = PrimaryButton(text="Confirm", icon="check", on_click=start_decryption, width=150)

    actions = ft.Row(
        controls=[back_btn, confirm_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40
    )

    content = ft.Column(
        controls=[
            ft.Container(height=40),
            file_container,
            ft.Container(height=20),
            password_container,
            ft.Container(height=80),
            actions
        ],
        width=500,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return ft.View(
        "/decrypt",
        controls=[
            file_picker,
            ft.Container(
                content=content,
                alignment=ft.alignment.center,
                expand=True
            )
        ],
        bgcolor=AppColors.BACKGROUND,
        padding=0
    )
