import spotipy

from rich import print
from spotipy.oauth2 import SpotifyOAuth

import utils

from ._base import Skill


class SpotifySkill(Skill):
    def __init__(self):
        self.sp = (
            spotipy.Spotify(
                auth_manager=SpotifyOAuth(
                    client_id=utils.get_env("SPOTIFY_ID"),
                    client_secret=utils.get_env("SPOTIFY_SECRET"),
                    redirect_uri="http://127.0.0.1:8888/callback",
                    scope="""
user-read-playback-state
user-read-currently-playing
user-modify-playback-state
user-top-read
""".replace("\n", " ").strip(),
                )
            ),
        )

    def get_currently_playing(self) -> dict:
        """Returns track, album, and artists."""
        # I tested it, it even works for local files, including album retrieval.

        current_track = self.sp[0].current_user_playing_track()

        if current_track is None:
            return {"error": "No track is currently playing."}

        item = current_track["item"]
        artists = "; ".join([artist["name"] for artist in item["artists"]])

        return {
            "track": item["name"],
            "artists": artists,
            "album": item["album"]["name"],
        }

    def search(self, query: str) -> dict:
        """Search for a track, album, or artist (all at once). Prefer tracks > albums > artists if the result is ambiguous, unless the query explicitly mentions otherwise."""
        results = self.sp[0].search(q=query, type="track,artist,album", limit=3)

        res = {"tracks": [], "artists": [], "albums": []}
        for track in results["tracks"]["items"]:
            res["tracks"].append(
                {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": "; ".join(
                        [artist["name"] for artist in track["artists"]]
                    ),
                }
            )

        for artist in results["artists"]["items"]:
            res["artists"].append(
                {
                    "id": artist["id"],
                    "name": artist["name"],
                }
            )

        for album in results["albums"]["items"]:
            res["albums"].append(
                {
                    "id": album["id"],
                    "name": album["name"],
                    "artists": "; ".join(
                        [artist["name"] for artist in album["artists"]]
                    ),
                }
            )

        return res

    def play_track_id(self, track_id: str) -> None:
        """Play a track by its Spotify ID."""
        self.sp[0].start_playback(uris=[f"spotify:track:{track_id}"])


if __name__ == "__main__":
    spotify_skill = SpotifySkill()
    # print(spotify_skill.get_currently_playing())
    # print(spotify_skill.search("toxicity"))
    spotify_skill.play_track_id("2DlHlPMa4M17kufBvI2lEN")
