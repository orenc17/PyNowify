from collections.abc import Callable
import tkinter as tk


class VectorIconButton(tk.Canvas):
    """A cross-platform, DPI-independent vector icon button rendered on Canvas."""

    def __init__(
        self, parent: tk.Widget, icon_type: str, command: Callable[[], None], **kwargs
    ) -> None:
        super().__init__(parent, width=32, height=32, highlightthickness=0, cursor="hand2", **kwargs)
        self.icon_type = icon_type
        self.command = command
        self.fg_color = "#ffffff"
        self.hover_color = "#b0b0b0"
        self.is_playing = False

        self.bind("<Button-1>", lambda e: self.command())
        self.bind("<Enter>", self.on_hover)
        self.bind("<Leave>", self.on_leave)

    def set_color(self, fg_color: str, hover_color: str) -> None:
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.redraw(self.fg_color)

    def set_state(self, is_playing: bool) -> None:
        if self.is_playing != is_playing:
            self.is_playing = is_playing
            self.redraw(self.fg_color)

    def on_hover(self, event: tk.Event) -> None:
        self.redraw(self.hover_color)

    def on_leave(self, event: tk.Event) -> None:
        self.redraw(self.fg_color)

    def redraw(self, color: str) -> None:
        self.delete("all")

        if self.icon_type == "prev":
            self.create_line(6, 8, 6, 24, fill=color, width=2.5)
            self.create_polygon(18, 8, 8, 16, 18, 24, fill=color)
            self.create_polygon(27, 8, 17, 16, 27, 24, fill=color)

        elif self.icon_type == "next":
            self.create_polygon(5, 8, 15, 16, 5, 24, fill=color)
            self.create_polygon(14, 8, 24, 16, 14, 24, fill=color)
            self.create_line(26, 8, 26, 24, fill=color, width=2.5)

        elif self.icon_type == "play_pause":
            if self.is_playing:
                self.create_rectangle(8, 7, 13, 25, fill=color, outline="")
                self.create_rectangle(19, 7, 24, 25, fill=color, outline="")
            else:
                self.create_polygon(9, 6, 26, 16, 9, 26, fill=color)
