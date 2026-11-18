# Home page of my portfolio app.
# Run with: streamlit run Home.py

import streamlit as st

from utils.data import DATASET_NAME, SOURCE_URL, load_data
from utils.ui import LINKEDIN, NAME, TAGLINE, WEBSITE, card, footer, setup_page

setup_page("Home")
df = load_data()

# ----- Hero banner -----
with st.container(key="hero"):
    st.caption("DATA VISUALIZATION PORTFOLIO")
    st.title(NAME)
    st.markdown("#### What makes a song popular on Spotify?")
    st.markdown(f"{TAGLINE}")
    col1, col2, col3 = st.columns([1, 1, 4])
    col1.link_button("LinkedIn", LINKEDIN, width="stretch")
    col2.link_button("Website", WEBSITE, width="stretch")

st.write("")

# ----- Quick facts -----
col1, col2, col3, col4 = st.columns(4)
col1.metric("Unique tracks", f"{len(df):,}")
col2.metric("Artists", f"{df['track_artist'].nunique():,}")
col3.metric("Playlist genres", df["genre"].nunique())
col4.metric("Release years", f"{df['release_year'].min()} - {df['release_year'].max()}")

st.write("")

# ----- Pages -----
st.subheader("Explore")
pages = [
    ("pages/1_Bio.py", "Bio", "Who I am, my tools, and how I think about visualization."),
    ("pages/2_EDA_Gallery.py", "EDA Gallery", "Six charts, each answering one question."),
    ("pages/3_Dashboard.py", "Dashboard", "Filter the data and watch the KPIs and charts update."),
    ("pages/4_Future_Work.py", "Future Work", "What's next, and how the app grew from a paper sketch."),
]
columns = st.columns(4)
for col, (path, label, text) in zip(columns, pages):
    with col:
        with card():
            st.markdown(f"#### {label}")
            st.caption(text)
            st.page_link(path, label="Open " + label)

st.write("")

# ----- About -----
with card():
    st.markdown("#### About this app")
    st.write(
        "A portfolio and a small analytics project in one. It looks at Spotify audio features "
        "(energy, danceability, mood, tempo) and popularity across six playlist genres."
    )
    st.caption(f"Data: [{DATASET_NAME}]({SOURCE_URL})")

footer()
