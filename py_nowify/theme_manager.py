from io import BytesIO
from typing import Optional
from colorthief import ColorThief
from PIL import Image, ImageTk


class ThemeManager:
    """Handles album art processing and dynamic color extraction."""

    @staticmethod
    def get_dynamic_theme(image_data: bytes) -> tuple[str, str, str, str, str, str]:
        """Extracts dynamic palette (bg, primary, secondary, tertiary, prog_bg, prog_fill)."""
        try:
            color_thief = ColorThief(BytesIO(image_data))
            dominant_color = color_thief.get_color(quality=1)
            r, g, b = dominant_color
            bg_hex = f"#{r:02x}{g:02x}{b:02x}"

            luminance = 0.299 * r + 0.587 * g + 0.114 * b

            if luminance > 140:
                return bg_hex, "#1a1a1a", "#3a3a3a", "#5a5a5a", "#a0a0a0", "#1a1a1a"
            return bg_hex, "#ffffff", "#d0d0d0", "#909090", "#2a2a2a", "#ffffff"
        except Exception:
            return "#121212", "#ffffff", "#d0d0d0", "#909090", "#2a2a2a", "#ffffff"

    @staticmethod
    def load_album_art(image_data: bytes, size: int) -> Optional[ImageTk.PhotoImage]:
        try:
            img = Image.open(BytesIO(image_data))
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error rendering image: {e}")
            return None
