import flet as ft

class AppColors:
    BACKGROUND = "#121212"  # Deep Black
    SURFACE = "#1E1E1E"     # Slightly lighter for cards/inputs
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#AAAAAA"
    ACCENT = "#2B2B2B"      # Button color
    ACCENT_HOVER = "#404040"
    ERROR = "#CF6679"
    SUCCESS = "#03DAC6"

class AppFonts:
    heading_font = "Space Grotesk"
    body_font = "Roboto"

class AppTextStyles:
    TITLE = ft.TextStyle(size=32, weight=ft.FontWeight.BOLD, letter_spacing=4, color=AppColors.TEXT_PRIMARY)
    SUBTITLE = ft.TextStyle(size=14, weight=ft.FontWeight.W_300, letter_spacing=3, color=AppColors.TEXT_SECONDARY)
    BUTTON = ft.TextStyle(size=16, weight=ft.FontWeight.W_500, color=AppColors.TEXT_PRIMARY)
