import flet as ft
from ui.styles import AppColors, AppTextStyles

class PrimaryButton(ft.ElevatedButton):
    def __init__(self, text, icon=None, on_click=None, width=None):
        super().__init__(
            text=text,
            icon=icon,
            on_click=on_click,
            width=width,
            height=50,
            style=ft.ButtonStyle(
                color=AppColors.TEXT_PRIMARY,
                bgcolor={"": AppColors.ACCENT, "hovered": AppColors.ACCENT_HOVER},
                shape=ft.RoundedRectangleBorder(radius=25),
                elevation=0,
            ),
        )

class InputField(ft.TextField):
    def __init__(self, hint_text, icon, password=False, can_reveal_password=False, read_only=False, suffix=None, **kwargs):
        super().__init__(
            **kwargs,
            hint_text=hint_text,
            password=password,
            can_reveal_password=can_reveal_password,
            read_only=read_only,
            prefix_icon=icon,
            suffix=suffix,
            border_color="transparent",
            bgcolor="transparent",
            text_style=ft.TextStyle(color=AppColors.TEXT_PRIMARY),
            hint_style=ft.TextStyle(color=AppColors.TEXT_SECONDARY),

            border_width=0,
            cursor_color=AppColors.TEXT_PRIMARY,
            height=50,
            content_padding=15
        )

class MinimalContainer(ft.Container):
    def __init__(self, content):
        super().__init__(
            content=content,
            bgcolor=AppColors.SURFACE,
            border_radius=10,
            padding=ft.padding.only(left=10, right=10)
        )

def show_dialog(page: ft.Page, title: str, message: str, is_error: bool = False):
    def close_dlg(e):
        page.close(dlg)

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(title, style=ft.TextStyle(color=AppColors.ERROR if is_error else AppColors.SUCCESS, weight="bold")),
        content=ft.Text(message, style=ft.TextStyle(color=AppColors.TEXT_PRIMARY)),
        actions=[
            ft.ElevatedButton(
                "OK", 
                on_click=close_dlg, 
                style=ft.ButtonStyle(
                    color=AppColors.TEXT_PRIMARY,
                    bgcolor={"": AppColors.ACCENT if not is_error else AppColors.ERROR},
                    shape=ft.RoundedRectangleBorder(radius=25),
                )
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=AppColors.SURFACE,
        shape=ft.RoundedRectangleBorder(radius=10),
    )
    
    page.open(dlg)
