from typing import Any, Optional
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from .config import AppConfig


class SpotifyService:
    """Handles Spotify authentication and API interactions."""

    def __init__(self, config: AppConfig) -> None:
        self.sp: spotipy.Spotify = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=config.client_id,
                client_secret=config.client_secret,
                redirect_uri=config.redirect_uri,
                scope=config.scope,
            )
        )

    def get_current_playback(self) -> Optional[dict[str, Any]]:
        """Fetches the user's current playback state from Spotify."""
        try:
            return self.sp.current_playback(additional_types="episode")
        except Exception as e:
            print(f"Spotify API Error: {e}")
            return None

    def next_track(self) -> None:
        try:
            self.sp.next_track()
        except Exception as e:
            print(f"Error skipping forward: {e}")

    def previous_track(self) -> None:
        try:
            self.sp.previous_track()
        except Exception as e:
            print(f"Error skipping back: {e}")

    def toggle_playback(self, is_playing: bool) -> None:
        try:
            if is_playing:
                self.sp.pause_playback()
            else:
                self.sp.start_playback()
        except Exception as e:
            print(f"Error toggling playback: {e}")
