"""
This module provides functionalities related to interacting with the Spotify API.

Imports:
    - datetime: Module for manipulating dates and times.
    - pathlib: Module for working with filesystem paths.
    - os: Module for interacting with the operating system.
    - requests: Module for making HTTP requests.
    - print: For enhanced output formatting.
    - load_dotenv: For loading environment variables from a .env file.
    - image: Module for image manipulation.
"""

import datetime
import requests
from typing import List, Tuple


class Spotify:
    """
    Uses Spotify's API to search and retrieve about a track.
    """

    def __init__(self, CLIENT_ID, CLIENT_SECRET):
        self.__CLIENT_ID = CLIENT_ID
        self.__CLIENT_SECRET = CLIENT_SECRET
        self.__BASE_URL = "https://api.spotify.com/v1"
        self.authorization_header()

    def authorization_header(self):
        """
        Constructs the authorization header required for API requests.
        """
        endpoint = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.__CLIENT_ID,
            "client_secret": self.__CLIENT_SECRET,
        }

        # Requesting token from Spotify API
        data = requests.post(endpoint, headers=headers, params=payload)
        token = data.json()["access_token"]

        self.__AUTH_HEADER = {"Authorization": f"Bearer {token}"}

    def search_track(self, track_name: str, limit: int = 5):
        """
        Searches for a track through Spotify's API and provides track information.

        Args:
            track_name (str): The name of the track to search.
            limit (bool, optional): Set the limit for the number songs to be shown.

        Returns:
            dict: Information about the selected track.
        """
        tracks = []

        query_params = {"q": track_name, "type": "track", "limit": limit}
        track_data = requests.get(
            f"{self.__BASE_URL}/search", params=query_params, headers=self.__AUTH_HEADER
        ).json()

        # Displaying search results to the user
        for i, item in enumerate(
            track_data.get("tracks", {}).get("items", [])[:10], start=1
        ):
            name = item["name"]
            artist = item["artists"][0]["name"]
            album = item["album"]["name"]
            trackid = item["id"]

            tracks.append([i, name, artist, album, trackid])

        return tracks

    def trackinfo(self, track: List[Tuple[int, str, str, str, str]]):
        t_data = requests.get(
            f"{self.__BASE_URL}/tracks/{track[4]}", headers=self.__AUTH_HEADER
        ).json()

        a_data = requests.get(
            f"{self.__BASE_URL}/albums/{t_data['album']['id']}",
            headers=self.__AUTH_HEADER,
        ).json()

        album_label = a_data["label"]

        # Formatting the release date
        date = t_data["album"]["release_date"]
        precision = t_data["album"]["release_date_precision"]
        date_format = {"day": "%Y-%m-%d", "month": "%Y-%m", "year": "%Y"}.get(
            precision, ""
        )
        release_date = datetime.datetime.strptime(date, date_format).strftime(
            "%B %d, %Y"
        )

        # Extracting track information
        info = {
            "album_id": t_data["album"]["id"],
            "name": t_data["name"],
            "artist": t_data["artists"][0]["name"],
            "year": t_data["album"]["release_date"],
            "duration": f"{(t_data['duration_ms'] // 60000):02d}:{(t_data['duration_ms'] // 1000 % 60):02d}",
            "image": t_data["album"]["images"][0]["url"],
            "label": f"{release_date}\n{album_label}",
            "track_id": t_data["id"],
            "cover": "./assets/spotify_banner.jpg"
        }

        return info
