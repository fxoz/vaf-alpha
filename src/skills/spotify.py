import spotipy
import logging

from rich import print
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

import utils

from .helpers import spotify_recommend
from ._base import Skill

for name in ["urllib3", "requests", "spotipy"]:
    logging.getLogger(name).setLevel(logging.CRITICAL)


class SpotifySkill(Skill):
    def __init__(self):
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=utils.get_env("SPOTIFY_ID"),
                client_secret=utils.get_env("SPOTIFY_SECRET"),
                redirect_uri="http://127.0.0.1:8888/callback",
                scope="user-read-playback-state user-read-currently-playing user-modify-playback-state user-top-read",
            )
        )
        # lazy cache because Spotify wants a device_id for playback control, unless there is a device that's currently playing music
        self._device_id: str | None = None

    def _get_device_id(self) -> str | None:
        """Fetch and cache the first available device ID."""
        devices = self.sp.devices().get("devices", [])
        if not devices:
            return None

        # Prefer the currently active device, otherwise take the first one
        active = next((d for d in devices if d["is_active"]), None)
        self._device_id = (active or devices[0])["id"]
        return self._device_id

    def _run_with_device(self, fn, *args, **kwargs):
        """
        Run a playback command, injecting a device_id.
        On 404, refreshes the device cache and retries once.
        """
        try:
            return fn(*args, device_id=self._device_id, **kwargs)
        except SpotifyException as e:
            if e.http_status == 404:
                self._device_id = self._get_device_id()
                if self._device_id is None:
                    raise RuntimeError("No Spotify devices available.") from e
                return fn(*args, device_id=self._device_id, **kwargs)
            raise

    # ── Playback controls ──────────────────────────────────────────────────

    def play_track_id(
        self, track_id: str, autoplay_similar_tracks: bool = True
    ) -> None:
        """Play a track by its Spotify ID. Only disable autoplay if the user asks for it."""
        # recs = (
        #     spotify_recommend.recommend_based_on_spotify_track(
        #         track_id=track_id, n_songs=20
        #     )
        #     if autoplay_similar_tracks
        #     else []
        # )
        self._run_with_device(
            self.sp.start_playback,
            uris=[f"spotify:track:{track_id}"],
        )

    def pause(self) -> None:
        """Pause playback."""
        self._run_with_device(self.sp.pause_playback)

    def resume(self) -> None:
        """Resume playback."""
        self._run_with_device(self.sp.start_playback)

    def next_track(self) -> None:
        """Skip to the next track."""
        self._run_with_device(self.sp.next_track)

    def set_volume(self, volume_percent: int) -> None:
        """Set the volume (0-100). Use get_volume() first unless user specifies a value."""
        self._run_with_device(self.sp.volume, volume_percent)

    # ── Read-only (no device needed) ──────────────────────────────────────

    def get_volume(self) -> int:
        """Get the current volume (0-100), or -1 if nothing is playing."""
        playback = self.sp.current_playback()
        if not playback:
            return -1
        return playback["device"]["volume_percent"]

    def get_currently_playing(self) -> dict:
        """Returns track, album, and artists."""
        current_track = self.sp.current_user_playing_track()
        if current_track is None:
            return {"error": "No track is currently playing."}
        item = current_track["item"]
        return {
            "track": item["name"],
            "artists": "; ".join(a["name"] for a in item["artists"]),
            "album": item["album"]["name"],
        }

    def search_anything(self, query: str) -> dict:
        """Search for a track, album, or artist. Prefer tracks > albums > artists."""
        results = self.sp.search(q=query, type="track,artist,album", limit=3)
        res = {"tracks": [], "artists": [], "albums": []}
        for track in results["tracks"]["items"]:
            res["tracks"].append(
                {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": "; ".join(a["name"] for a in track["artists"]),
                }
            )
        for artist in results["artists"]["items"]:
            res["artists"].append({"id": artist["id"], "name": artist["name"]})
        for album in results["albums"]["items"]:
            res["albums"].append(
                {
                    "id": album["id"],
                    "name": album["name"],
                    "artists": "; ".join(a["name"] for a in album["artists"]),
                }
            )
        return res

    def list_devices(self) -> list[dict]:
        """List available Spotify Connect devices."""
        devices = self.sp.devices()
        return [
            {
                "id": d["id"],
                "name": d["name"],
                "type": d["type"],
                "is_currently_playing": d["is_active"],
            }
            for d in devices["devices"]
        ]


if __name__ == "__main__":
    skill = SpotifySkill()
    print(skill.resume())
