from collections.abc import Callable
import math
import tkinter as tk
from tkinter import font
from typing import Optional

from ..config import AppConfig
from ..theme_manager import ThemeManager
from .widgets import VectorIconButton


class NowifyUI:
    """Manages screen configurations, window geometry, layout, and styling."""

    def __init__(
        self,
        root: tk.Tk,
        config: AppConfig,
        on_prev: Callable[[], None],
        on_play_pause: Callable[[], None],
        on_next: Callable[[], None],
    ) -> None:
        self.root: tk.Tk = root
        self.config: AppConfig = config
        self.current_orientation: str = "horizontal"
        self.current_fg: str = "white"
        self.current_hover_fg: str = "#b0b0b0"
        self.album_art_size: int = 140
        self.progress_width: int = 220

        self._resize_job: Optional[str] = None
        self._last_width: int = 0
        self._last_height: int = 0

        self._init_fonts()
        self._init_widgets(on_prev, on_play_pause, on_next)
        self._configure_window()

    @staticmethod
    def get_wm_aspect(width: int, height: int) -> tuple[int, int, int, int]:
        divisor = math.gcd(width, height)
        numerator = width // divisor
        denominator = height // divisor
        return numerator, denominator, numerator, denominator

    @staticmethod
    def ms_to_min_sec(ms: int) -> str:
        seconds = max(0, int(ms / 1000))
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"

    def _configure_window(self) -> None:
        if self.config.fullscreen:
            screen_w = self.root.winfo_screenwidth()
            screen_h = self.root.winfo_screenheight()
        else:
            screen_w = self.config.window_width
            screen_h = self.config.window_height

        self.root.geometry(f"{screen_w}x{screen_h}")
        self.root.configure(bg="#121212")
        self.root.resizable(self.config.resizable, self.config.resizable)

        if self.config.lock_aspect_ratio:
            self.root.aspect(*self.get_wm_aspect(screen_w, screen_h))

        self._apply_layout(screen_w, screen_h)
        self.root.bind("<Configure>", self.on_window_resize)

    def _init_fonts(self) -> None:
        self.track_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.artist_font = font.Font(family="Helvetica", size=13)
        self.album_font = font.Font(family="Helvetica", size=11)
        self.time_font = font.Font(family="Helvetica", size=10)

    def _init_widgets(
        self,
        on_prev: Callable[[], None],
        on_play_pause: Callable[[], None],
        on_next: Callable[[], None],
    ) -> None:
        self.main_container = tk.Frame(self.root, bg="#121212")
        self.main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.left_frame = tk.Frame(self.main_container, bg="#121212")
        self.album_art_label = tk.Label(self.left_frame, bg="#121212", bd=0)
        self.album_art_label.pack()

        self.right_frame = tk.Frame(self.main_container, bg="#121212")

        self.track_label = tk.Label(
            self.right_frame, text="Loading...", font=self.track_font, fg="white", bg="#121212"
        )
        self.track_label.pack(pady=(0, 4))

        self.artist_label = tk.Label(
            self.right_frame, text="", font=self.artist_font, fg="#d0d0d0", bg="#121212"
        )
        self.artist_label.pack(pady=(0, 2))

        self.album_label = tk.Label(
            self.right_frame, text="", font=self.album_font, fg="#909090", bg="#121212"
        )
        self.album_label.pack(pady=(0, 15))

        self.progress_canvas = tk.Canvas(
            self.right_frame, height=5, bg="#2a2a2a", highlightthickness=0
        )
        self.progress_fill = self.progress_canvas.create_rectangle(0, 0, 0, 5, fill="white", width=0)

        self.time_frame = tk.Frame(self.right_frame, bg="#121212")
        self.current_time_label = tk.Label(
            self.time_frame, text="0:00", font=self.time_font, fg="#909090", bg="#121212"
        )
        self.current_time_label.pack(side=tk.LEFT)
        self.duration_label = tk.Label(
            self.time_frame, text="0:00", font=self.time_font, fg="#909090", bg="#121212"
        )
        self.duration_label.pack(side=tk.RIGHT)

        self.controls_frame = tk.Frame(self.right_frame, bg="#121212")
        self.prev_btn = VectorIconButton(self.controls_frame, "prev", on_prev, bg="#121212")
        self.prev_btn.pack(side=tk.LEFT, padx=12)

        self.play_pause_btn = VectorIconButton(
            self.controls_frame, "play_pause", on_play_pause, bg="#121212"
        )
        self.play_pause_btn.pack(side=tk.LEFT, padx=12)

        self.next_btn = VectorIconButton(self.controls_frame, "next", on_next, bg="#121212")
        self.next_btn.pack(side=tk.LEFT, padx=12)

    def on_window_resize(self, event: tk.Event) -> None:
        if event.widget != self.root:
            return

        if event.width == self._last_width and event.height == self._last_height:
            return

        self._last_width = event.width
        self._last_height = event.height

        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)

        self._resize_job = self.root.after(
            50, lambda: self._apply_layout(event.width, event.height)
        )

    def _apply_layout(self, width: int, height: int) -> None:
        self._resize_job = None
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()
        self.current_orientation = "horizontal" if width >= height else "vertical"

        if self.current_orientation == "horizontal":
            self.root.minsize(580, 350)
            self.left_frame.pack(side=tk.LEFT, anchor=tk.CENTER, padx=(0, int(width * 0.04)))
            self.right_frame.pack(side=tk.LEFT, anchor=tk.CENTER)
            for widget in (self.track_label, self.artist_label, self.album_label):
                widget.config(anchor="w", justify="left")
            self.album_art_size = max(140, int(height * 0.68))
            self.progress_width = max(220, int(width * 0.42))
            track_sz = max(12, int(height * 0.05))
            artist_sz = max(9, int(height * 0.035))
            album_sz = max(8, int(height * 0.028))
        else:
            self.root.minsize(320, 420)
            self.left_frame.pack(side=tk.TOP, anchor=tk.CENTER, pady=(0, int(height * 0.03)))
            self.right_frame.pack(side=tk.TOP, anchor=tk.CENTER)
            for widget in (self.track_label, self.artist_label, self.album_label):
                widget.config(anchor="center", justify="center")
            self.album_art_size = max(130, int(width * 0.52))
            self.progress_width = max(200, int(width * 0.72))
            track_sz = max(12, int(width * 0.055))
            artist_sz = max(9, int(width * 0.038))
            album_sz = max(8, int(width * 0.03))

        self.track_font.config(size=track_sz)
        self.artist_font.config(size=artist_sz)
        self.album_font.config(size=album_sz)

        self.progress_canvas.config(width=self.progress_width)
        self.time_frame.config(width=self.progress_width)
        self.track_label.config(wraplength=self.progress_width)

    def update_playback_state(self, progress_ms: int, duration_ms: int, is_playing: bool) -> None:
        safe_duration = max(1, duration_ms)
        safe_progress = max(0, progress_ms)

        progress_ratio = min(safe_progress / safe_duration, 1.0)
        fill_width = int(self.progress_width * progress_ratio)
        self.progress_canvas.coords(self.progress_fill, 0, 0, fill_width, 5)

        self.current_time_label.config(text=self.ms_to_min_sec(safe_progress))
        self.duration_label.config(text=self.ms_to_min_sec(safe_duration))
        self.play_pause_btn.set_state(is_playing)

    def update_album_art(self, image_data: Optional[bytes]) -> None:
        if image_data:
            photo = ThemeManager.load_album_art(image_data, self.album_art_size)
            if photo:
                self.album_art_label.config(image=photo)
                self.album_art_label.image = photo
        else:
            self.album_art_label.config(image="")

    def show_playing_elements(self) -> None:
        if not self.progress_canvas.winfo_ismapped():
            self.progress_canvas.pack(pady=(0, 5))
        if not self.time_frame.winfo_ismapped():
            self.time_frame.pack(fill=tk.X, pady=(0, 15))
        if not self.controls_frame.winfo_ismapped():
            self.controls_frame.pack(pady=(5, 0))

    def hide_playing_elements(self) -> None:
        self.progress_canvas.pack_forget()
        self.time_frame.pack_forget()
        self.controls_frame.pack_forget()

    def apply_theme(
        self,
        theme: tuple[str, str, str, str, str, str],
        track_name: str,
        artist_name: str,
        album_name: str,
    ) -> None:
        bg_color, primary_fg, secondary_fg, tertiary_fg, prog_bg, prog_fill = theme
        self.current_fg = primary_fg
        self.current_hover_fg = "#b0b0b0" if primary_fg in ("#ffffff", "white") else "#888888"

        for widget in (
            self.root,
            self.main_container,
            self.left_frame,
            self.right_frame,
            self.time_frame,
            self.controls_frame,
        ):
            widget.config(bg=bg_color)

        self.track_label.config(text=track_name, bg=bg_color, fg=primary_fg)
        self.artist_label.config(text=artist_name, bg=bg_color, fg=secondary_fg)
        self.album_label.config(text=album_name, bg=bg_color, fg=tertiary_fg)
        self.current_time_label.config(bg=bg_color, fg=tertiary_fg)
        self.duration_label.config(bg=bg_color, fg=tertiary_fg)

        for btn in (self.prev_btn, self.play_pause_btn, self.next_btn):
            btn.config(bg=bg_color)
            btn.set_color(primary_fg, self.current_hover_fg)

        self.progress_canvas.config(bg=prog_bg)
        self.progress_canvas.itemconfig(self.progress_fill, fill=prog_fill)

    def reset_to_idle(self) -> None:
        self.hide_playing_elements()
        self.track_label.config(text="Nothing playing", fg="white", bg="#121212")
        self.artist_label.config(text="", fg="#d0d0d0", bg="#121212")
        self.album_label.config(text="", fg="#909090", bg="#121212")
        self.update_album_art(None)
        self.current_fg = "white"

        for widget in (self.root, self.main_container, self.left_frame, self.right_frame):
            widget.config(bg="#121212")
