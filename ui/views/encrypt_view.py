import flet as ft
import os
import threading
from ui.styles import AppColors
from ui.components import PrimaryButton, InputField, MinimalContainer, show_dialog
from core.file_utils import FileUtils
from core.crypto import CryptoService

def encrypt_view(page: ft.Page):
    folder_input = InputField(
        hint_text="Select folder", 
        icon="folder", 
        read_only=True
    )
    
    password_input = InputField(
        hint_text="Password", 
        icon="lock", 
        password=True, 
        can_reveal_password=True
    )

    def on_folder_picked(e: ft.FilePickerResultEvent):
        if e.path:
            folder_input.value = e.path
            folder_input.update()

    file_picker = ft.FilePicker(on_result=on_folder_picked)

    def select_folder(e):
        file_picker.get_directory_path()

    folder_container = ft.Stack(
        controls=[
            MinimalContainer(folder_input),
            ft.Container(
                on_click=select_folder,
                bgcolor=ft.Colors.TRANSPARENT,
                height=50,
                width=500,
            )
        ]
    )
    
    password_container = MinimalContainer(password_input)

    delete_original_checkbox = ft.Checkbox(
        label="Delete original folder after encryption",
        value=False,
        label_style=ft.TextStyle(color=AppColors.TEXT_SECONDARY, size=14),
        fill_color={
            ft.ControlState.HOVERED: AppColors.ACCENT,
            ft.ControlState.FOCUSED: AppColors.ACCENT,
            ft.ControlState.DEFAULT: AppColors.SURFACE,
            ft.ControlState.SELECTED: AppColors.ACCENT,
        },
        check_color=AppColors.TEXT_PRIMARY
    )

    def go_back(e):
        page.go("/")

    def start_encryption(e):
        path = folder_input.value
        pwd = password_input.value
        should_delete = delete_original_checkbox.value
        
        if not path or not pwd:
            show_dialog(page, "Error", "Please select a folder and enter a password", is_error=True)
            return

        confirm_btn.text = "Encrypting..."
        confirm_btn.disabled = True
        confirm_btn.update()

        def process():
            try:
                zip_path = FileUtils.zip_folder(path)
                CryptoService.encrypt_file(zip_path, pwd)
                FileUtils.cleanup_file(zip_path)
                
                success_msg = "Folder encrypted successfully!"
                
                if should_delete:
                    import shutil
                    if os.path.exists(path):
                        shutil.rmtree(path)
                    success_msg += "\nOriginal folder deleted."

                show_dialog(page, "Success", success_msg, is_error=False)
            except Exception as ex:
                 show_dialog(page, "Error", f"Encryption failed: {str(ex)}", is_error=True)
            finally:
                confirm_btn.text = "Confirm"
                confirm_btn.disabled = False
                page.update()

        threading.Thread(target=process).start()

    back_btn = PrimaryButton(text="Back", icon="arrow_back", on_click=go_back, width=120)
    confirm_btn = PrimaryButton(text="Confirm", icon="check", on_click=start_encryption, width=150)

    actions = ft.Row(
        controls=[back_btn, confirm_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=40
    )

    content = ft.Column(
        controls=[
            ft.Container(height=40),
            folder_container,
            ft.Container(height=20),
            password_container,
            ft.Container(height=10),
            delete_original_checkbox,
            ft.Container(height=70),
            actions
        ],
        width=500,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return ft.View(
        "/encrypt",
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
