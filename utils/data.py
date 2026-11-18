# Loads and cleans the Spotify dataset. Every page uses load_data() from here.

import os

import pandas as pd
import streamlit as st

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "spotify_songs.csv")

DATASET_NAME = "Spotify Songs (TidyTuesday, 2020-01-21)"
SOURCE_URL = "https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21"

# Nicer names for the genre column
GENRE_NAMES = {
    "edm": "EDM",
    "latin": "Latin",
    "pop": "Pop",
    "r&b": "R&B",
    "rap": "Rap",
    "rock": "Rock",
}


# cache_data means the CSV is only read once instead of on every click
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    # 5 rows are missing the track name and artist, so drop them
    df = df.dropna(subset=["track_name", "track_artist"])

    # The same song can be in more than one playlist, so keep only one copy
    df = df.drop_duplicates(subset="track_id", keep="first")

    # Some release dates are just a year ("2012"), so take the first 4 characters
    df["release_year"] = df["track_album_release_date"].str[:4].astype(int)

    # Extra columns that are easier to read
    df["duration_min"] = df["duration_ms"] / 60000
    df["genre"] = df["playlist_genre"].map(GENRE_NAMES)
    df["subgenre"] = df["playlist_subgenre"].str.title()
    df["key_mode"] = df["mode"].map({1: "Major", 0: "Minor"})

    return df


# The songs and popularity scores were collected in January 2020 and the file has not
# changed since. DOWNLOADED is the date I copied the CSV into this project.
DATA_COLLECTED = "January 2020"
DOWNLOADED = "2026-11-18"
