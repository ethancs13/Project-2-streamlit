# Future Work page: next steps and what changed from my Lab 4.3 paper prototype.

import os

import streamlit as st

from utils.ui import STATS_FU, card, footer, page_header, setup_page

setup_page("Future Work")

PROTOTYPE = os.path.join(os.path.dirname(__file__), "..", "assets", "prototype.png")

page_header("Future Work", "Where I want to take this next, and how the app changed from my paper prototype")


# ----- Next steps (one card each) -----
st.subheader("Next steps")

steps = [
    ("1", "Fix remastered and re-released tracks",
     "551 of the 4,305 Rock tracks have \"Remaster\" in the name, so their release year is "
     "probably the remaster date, not the original. I plan to match these tracks by song name and "
     "artist to their earliest release, or drop them if no match is found. Then I'll re-check the "
     "Genre Trends chart, since the \"older Rock songs score higher\" finding may change."),
    ("2", "Popularity then vs. now",
     f"Every popularity score here is from January 2020. I already built [stats.fu]({STATS_FU}), a Spotify stats app "
     "that logs in with Spotify and reads track popularity, so I can reuse its login to pull today's "
     "popularity for the same track IDs and compare the two. That would show which songs and genres "
     "grew or faded. Spotify stopped giving new apps audio features in November 2024, so this "
     "comparison would cover popularity only."),
    ("3", "Explain the zero-popularity tracks",
     "2,616 tracks (about 9%) score exactly 0. Only 329 of them are a copy of a song that has a "
     "real score somewhere else, so duplicates explain just part of it. Next I'll check album type "
     "(compilations, re-releases), subgenre and playlist to find edge cases, then decide whether "
     "to exclude zeros by default or flag them."),
    ("4", "Song lookup",
     "A search box on the dashboard where you type a song or artist and see that track's energy, "
     "danceability, valence and tempo next to its genre's average. It would also mark where the "
     "song falls in the popularity distribution."),
]

# Show the cards 2 per row
row1 = st.columns(2)
row2 = st.columns(2)
all_columns = row1 + row2
for col, (number, title, text) in zip(all_columns, steps):
    with col:
        with card():
            st.markdown(f"##### :green[{number}.] {title}")
            st.caption(text)


# ----- Reflection -----
st.write("")
st.subheader("From paper prototype to final app")

left, right = st.columns(2)
with left:
    with card():
        st.markdown("##### :gray[Lab 4.3 prototype]")
        st.markdown(
            "- Home energy data (\"Xcel Grid Planner\")\n"
            "- Six sidebar filters\n"
            "- KPI row: total kWh, average kWh, peak month\n"
            "- Q1 line chart with kWh and temperature together\n"
            "- Two bar charts, a grouped bar chart, and insights"
        )
        if os.path.exists(PROTOTYPE):
            st.image(PROTOTYPE, caption="My Lab 4.3 paper prototype",
                     alt="Wireframe of a dashboard with a filter sidebar, a KPI row, a line "
                         "chart, two bar charts, a grouped bar chart and an insights box.")
with right:
    with card():
        st.markdown("##### :green[Final app]")
        st.markdown(
            "- Spotify songs data (the project required a new dataset)\n"
            "- Five filters, and subgenre only shows options for the chosen genres\n"
            "- KPIs compare the selection to all tracks\n"
            "- Q1 split into two charts instead of one chart with two y-axes\n"
            "- Same layout, plus a data source badge, refresh date, and limitations"
        )

st.write("")
col1, col2, col3 = st.columns(3)
with col1:
    with card():
        st.markdown("**Kept the layout**")
        st.caption("Filters on the left, KPIs on top, charts labeled Q1 to Q4, insights at the bottom.")
with col2:
    with card():
        st.markdown("**Fixed a misleading chart**")
        st.caption("Two y-axes on one chart can make any two lines look related, so I split them.")
with col3:
    with card():
        st.markdown("**Added context**")
        st.caption("Data source, refresh date, comparisons to all tracks, and a limitations note.")

footer()
