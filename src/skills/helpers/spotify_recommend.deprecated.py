import httpx


def _normalize_track_id(track_id: str) -> str:
    track_id = track_id.strip()

    if "spotify:track:" in track_id:
        track_id = track_id.split("spotify:track:", 1)[1]
    elif "open.spotify.com/track/" in track_id:
        track_id = track_id.split("open.spotify.com/track/", 1)[1]

    return track_id.split("?", 1)[0]


def recommend_based_on_spotify_track(track_id: str, n_songs: int = 5) -> list[str]:
    """Returns a list of Spotify track IDs recommended based on the given track ID."""
    track_id = _normalize_track_id(track_id)

    with httpx.Client(timeout=10.0) as client:
        res = client.get(
            "https://api.reccobeats.com/v1/track/recommendation",
            params={"size": n_songs, "seeds": [track_id, track_id, track_id]},
            headers={"Accept": "application/json"},
        )
        res.raise_for_status()
        open("reccobeats_response.json", "w").write(res.text)  # For debugging
        return [song["href"].split("/")[-1] for song in res.json()["content"]]


if __name__ == "__main__":
    track_id = (
        "https://open.spotify.com/track/2jSJm3Gv6GLxduWLenmjKS?si=61044b2572d141b0"
    )
    recommendations = recommend_based_on_spotify_track(track_id, n_songs=10)
    print(recommendations)
