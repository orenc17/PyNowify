import json
from typing import Optional
from dotenv import dotenv_values


class AppConfig:
    """Loads, parses, and validates application configuration from the environment."""

    def __init__(self, env_path: str = ".env") -> None:
        config = dotenv_values(env_path)

        self.fullscreen: bool = bool(json.loads(config.get("FULLSCREEN", "false").lower()))
        self.window_height: int = int(config.get("WINDOW_HEIGHT", 480))
        self.window_width: int = int(config.get("WINDOW_WIDTH", 800))
        self.lock_aspect_ratio: bool = bool(json.loads(config.get("LOCK_ASPECT_RATIO", "false").lower()))
        self.resizable: bool = bool(json.loads(config.get("RESIZEABLE", "false").lower()))

        self.client_id: Optional[str] = config.get("SPOTIPY_CLIENT_ID")
        self.client_secret: Optional[str] = config.get("SPOTIPY_CLIENT_SECRET")
        self.redirect_uri: Optional[str] = config.get("SPOTIPY_REDIRECT_URI")
        self.scope: str = (
            "user-read-currently-playing user-read-playback-state user-modify-playback-state"
        )

        self._validate()

    def _validate(self) -> None:
        assert self.client_id, "SPOTIPY_CLIENT_ID is missing or empty in the .env file."
        assert self.client_secret, "SPOTIPY_CLIENT_SECRET is missing or empty in the .env file."
        assert self.redirect_uri, "SPOTIPY_REDIRECT_URI is missing or empty in the .env file."
