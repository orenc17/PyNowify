from collections.abc import Callable
import threading
import tkinter as tk
from typing import Any, Optional
import requests

from .config import AppConfig
from .spotify_service import SpotifyService
from .theme_manager import ThemeManager
from .ui import NowifyUI


class NowifyApp:
    """Main application coordinator."""

    def __init__(self) -> None:
        self.root: tk.Tk = tk.Tk()
        self.root.title("Nowify")

        self.config: AppConfig = AppConfig()
        self.spotify: SpotifyService = SpotifyService(self.config)
        self.ui: NowifyUI = NowifyUI(
            self.root, self.config, self.prev_track, self.toggle_play_pause, self.next_track
        )

        self.current_track_id: Optional[str] = None
        self.current_image_data: Optional[bytes] = None
        self.is_playing: bool = False
        self.progress_ms: int = 0
        self.duration_ms: int = 1

        self.poll_spotify_loop()
        self.tick_progress_loop()

    def run(self) -> None:
        self.root.mainloop()

    def run_in_thread(self, target: Callable[..., Any], *args: Any) -> None:
        threading.Thread(target=target, args=args, daemon=True).start()

    def prev_track(self) -> None:
        self.run_in_thread(self._action_and_refresh, self.spotify.previous_track)

    def toggle_play_pause(self) -> None:
        self.run_in_thread(self._action_and_refresh, lambda: self.spotify.toggle_playback(self.is_playing))

    def next_track(self) -> None:
        self.run_in_thread(self._action_and_refresh, self.spotify.next_track)

    def _action_and_refresh(self, action: Callable[[], None]) -> None:
        action()
        self._fetch_spotify_state()

    def poll_spotify_loop(self) -> None:
        self.run_in_thread(self._fetch_spotify_state)
        self.root.after(5000, self.poll_spotify_loop)

    def tick_progress_loop(self) -> None:
        if self.is_playing and self.current_track_id is not None:
            self.progress_ms += 1000
            self.ui.update_playback_state(self.progress_ms, self.duration_ms, self.is_playing)
        self.root.after(1000, self.tick_progress_loop)

    def _fetch_spotify_state(self) -> None:
        try:
            playback = self.spotify.get_current_playback()

            if playback and playback.get("item"):
                is_playing = playback.get("is_playing", False)
                item = playback["item"]
                track_id = item.get("id") or item.get("uri") or item.get("name")
                progress_ms = playback.get("progress_ms", 0)
                duration_ms = item.get("duration_ms", 1)

                if track_id != self.current_track_id:
                    item_type = item.get("type")

                    if item_type == "episode":
                        track_name = item["name"]
                        artist_name = item.get("show", {}).get("publisher", "")
                        album_name = item.get("show", {}).get("name", "")
                        images = item.get("images", []) or item.get("show", {}).get("images", [])
                        album_cover_url = images[0]["url"] if images else None
                    else:
                        track_name = item["name"]
                        artist_name = ", ".join([artist["name"] for artist in item.get("artists", [])])
                        album_name = item.get("album", {}).get("name", "")
                        album_images = item.get("album", {}).get("images", [])
                        album_cover_url = album_images[0]["url"] if album_images else None

                    image_data = None
                    if album_cover_url:
                        try:
                            response = requests.get(album_cover_url, timeout=5)
                            image_data = response.content
                        except requests.RequestException as e:
                            print(f"Network Error fetching album art: {e}")

                    theme = (
                        ThemeManager.get_dynamic_theme(image_data)
                        if image_data
                        else ("#121212", "#ffffff", "#d0d0d0", "#909090", "#2a2a2a", "#ffffff")
                    )

                    self.root.after_idle(
                        self._apply_new_track_ui,
                        track_id,
                        image_data,
                        theme,
                        track_name,
                        artist_name,
                        album_name,
                        progress_ms,
                        duration_ms,
                        is_playing,
                    )
                else:
                    self.root.after_idle(
                        self._sync_playback_ui, progress_ms, duration_ms, is_playing
                    )

            else:
                self.root.after_idle(self._apply_idle_ui)

        except Exception as e:
            print(f"Background Thread Error: {e}")

    def _apply_new_track_ui(
        self,
        track_id: str,
        image_data: Optional[bytes],
        theme: tuple[str, str, str, str, str, str],
        track_name: str,
        artist_name: str,
        album_name: str,
        progress_ms: int,
        duration_ms: int,
        is_playing: bool,
    ) -> None:
        self.current_track_id = track_id
        self.current_image_data = image_data
        self.progress_ms = progress_ms
        self.duration_ms = duration_ms
        self.is_playing = is_playing

        self.ui.show_playing_elements()
        self.ui.apply_theme(theme, track_name, artist_name, album_name)
        self.ui.update_album_art(image_data)
        self.ui.update_playback_state(progress_ms, duration_ms, is_playing)

    def _sync_playback_ui(self, progress_ms: int, duration_ms: int, is_playing: bool) -> None:
        self.progress_ms = progress_ms
        self.duration_ms = duration_ms
        self.is_playing = is_playing
        self.ui.update_playback_state(progress_ms, duration_ms, is_playing)

    def _apply_idle_ui(self) -> None:
        if self.current_track_id is not None or self.ui.track_label.cget("text") == "Loading...":
            self.current_track_id = None
            self.current_image_data = None
            self.is_playing = False
            self.ui.reset_to_idle()
