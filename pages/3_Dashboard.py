# Dashboard page. The sidebar filters change the KPIs and all of the charts.
# Layout is based on my Lab 4.3 paper prototype:
# filters on the left, KPIs on top, Q1 line charts, Q2 and Q3 bars side by side,
# Q4 grouped bar, then insights at the bottom.

import plotly.express as px
import streamlit as st

from utils.data import DATA_COLLECTED, DATASET_NAME, DOWNLOADED, SOURCE_URL, load_data
from utils.ui import (GENRE_COLORS, GENRES, GREEN, LIGHT_GRAY, SOURCE_CAPTION, card, footer,
                      page_header, score_bar, setup_page)

setup_page("Dashboard")
df = load_data()


# ----- Sidebar filters -----
st.sidebar.header("Filters")

genres = st.sidebar.multiselect("Playlist genre", GENRES, default=GENRES)

# Only show subgenres that belong to the genres picked above
subgenre_options = sorted(df[df["genre"].isin(genres)]["subgenre"].unique())
subgenres = st.sidebar.multiselect("Subgenre (optional)", subgenre_options,
                                   placeholder="All subgenres")

years = st.sidebar.slider("Album release year", 1957, 2020, (1980, 2020))

modes = st.sidebar.multiselect("Key mode", ["Major", "Minor"], default=["Major", "Minor"])

popularity = st.sidebar.slider("Track popularity (0-100)", 0, 100, (0, 100))

# Apply the filters
filtered = df[
    (df["genre"].isin(genres))
    & (df["release_year"] >= years[0])
    & (df["release_year"] <= years[1])
    & (df["key_mode"].isin(modes))
    & (df["track_popularity"] >= popularity[0])
    & (df["track_popularity"] <= popularity[1])
]
if subgenres:
    filtered = filtered[filtered["subgenre"].isin(subgenres)]


# ----- Title and data source -----
page_header("Spotify Popularity Dashboard",
            "Use the filters in the sidebar. The KPIs and every chart update together.")
st.markdown(
    f"[![Data source](https://img.shields.io/badge/data_source-TidyTuesday_Spotify_Songs-1DB954)]({SOURCE_URL}) "
    f"&nbsp; Data collected: **{DATA_COLLECTED}** | Last refreshed (downloaded from TidyTuesday): "
    f"**{DOWNLOADED}**"
)

if len(filtered) == 0:
    st.warning("No tracks match these filters. Try a wider year or popularity range.")
    st.stop()


# ----- KPIs (hover the ? icon on each one for an explanation) -----
col1, col2, col3, col4 = st.columns(4)

col1.metric("Tracks in selection", f"{len(filtered):,}",
            f"{len(filtered) / len(df):.0%} of all tracks", delta_color="primary", delta_arrow="off")

# Most popular track in the selection. Names that don't fit end in "..." (hover for the full name).
top_track = filtered.loc[filtered["track_popularity"].idxmax()]
col2.metric("Most popular track", top_track["track_name"],
            f"{top_track['track_artist']} ({top_track['track_popularity']}/100)",
            delta_color="primary", delta_arrow="off",
            help=f"{top_track['track_name']} by {top_track['track_artist']} has the highest "
                 "Spotify popularity score in the current selection. Spotify scores every track "
                 "from 0 to 100 based on how many recent plays it has.")

# Danceability is a 0-1 score, so turn it into words too
avg_dance = round(filtered["danceability"].mean(), 2)
if avg_dance >= 0.66:
    dance_words = "Very danceable"
elif avg_dance >= 0.33:
    dance_words = "Somewhat danceable"
else:
    dance_words = "Not very danceable"
# Show it as a bar from 0 to 1 instead of a plain number
with col3:
    score_bar("Avg danceability", avg_dance, dance_words,
              "Spotify's danceability score goes from 0 (hard to dance to) to 1 (very easy to "
              "dance to). It is based on tempo, how steady the rhythm is, and beat strength.")

peak_year = filtered["release_year"].mode()[0]
peak_count = (filtered["release_year"] == peak_year).sum()
col4.metric("Peak release year", str(peak_year), f"{peak_count:,} tracks released",
            delta_color="primary", delta_arrow="off",
            help="The album release year with the most tracks in the current selection.")


# ----- Q1: line charts by year -----
st.subheader("Q1. Are newer songs more popular, and has energy changed?")

# Average per year, only for years with at least 10 tracks
by_year = filtered.groupby("release_year").agg(
    tracks=("track_id", "count"),
    popularity=("track_popularity", "mean"),
    energy=("energy", "mean"),
).reset_index()
by_year = by_year[by_year["tracks"] >= 10]

if len(by_year) == 0:
    st.info("Not enough tracks per year to draw this chart (need at least 10).")
else:
    # Two separate charts instead of one chart with two y-axes, which can be misleading
    left, right = st.columns(2)
    with left:
        fig = px.line(by_year, x="release_year", y="popularity", markers=True,
                      hover_data={"tracks": True},
                      title="Average popularity by release year",
                      labels={"release_year": "Album release year",
                              "popularity": "Average popularity (0-100)", "tracks": "Tracks"},
                      color_discrete_sequence=[GREEN], height=340)
        fig.update_layout(yaxis_range=[0, 100])
        st.plotly_chart(fig, width="stretch")
    with right:
        fig = px.line(by_year, x="release_year", y="energy", markers=True,
                      hover_data={"tracks": True},
                      title="Average energy by release year",
                      labels={"release_year": "Album release year",
                              "energy": "Average energy (0-1)", "tracks": "Tracks"},
                      color_discrete_sequence=[LIGHT_GRAY], height=340)
        fig.update_layout(yaxis_range=[0, 1])
        st.plotly_chart(fig, width="stretch")
    st.caption("Only years with 10 or more tracks in the selection are shown.")


# ----- Q2 and Q3: bar charts side by side -----
left, right = st.columns(2)

with left:
    st.subheader("Q2. Which genre is the most popular?")
    by_genre = filtered.groupby("genre").agg(
        median_popularity=("track_popularity", "median"),
        tracks=("track_id", "count"),
    ).reset_index().sort_values("median_popularity", ascending=False)

    fig = px.bar(by_genre, x="genre", y="median_popularity", color="genre",
                 color_discrete_map=GENRE_COLORS, text="median_popularity",
                 hover_data={"tracks": True},
                 title="Median popularity by genre",
                 labels={"genre": "Playlist genre", "median_popularity": "Median popularity (0-100)",
                         "tracks": "Tracks"},
                 height=420)
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(showlegend=False, yaxis_range=[0, 100])
    st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Q3. Which subgenres stand out?")
    by_sub = filtered.groupby(["subgenre", "genre"]).agg(
        median_popularity=("track_popularity", "median"),
        tracks=("track_id", "count"),
    ).reset_index()
    # Only subgenres with 20+ tracks, then the top 12
    by_sub = by_sub[by_sub["tracks"] >= 20]
    by_sub = by_sub.sort_values("median_popularity", ascending=False).head(12)

    fig = px.bar(by_sub, x="median_popularity", y="subgenre", color="genre", orientation="h",
                 color_discrete_map=GENRE_COLORS, text="median_popularity",
                 hover_data={"tracks": True},
                 title="Top 12 subgenres by median popularity (20+ tracks)",
                 labels={"subgenre": "Subgenre", "median_popularity": "Median popularity (0-100)",
                         "genre": "Genre", "tracks": "Tracks"},
                 height=420)
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    # Highest bar on top
    fig.update_layout(xaxis_range=[0, 100], yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, width="stretch")


# ----- Q4: grouped bar chart -----
st.subheader("Q4. How does each genre sound?")
features = ["danceability", "energy", "valence"]
sound = filtered.groupby("genre")[features].mean().reset_index()
# Reshape so each row is one genre + one feature
sound = sound.melt(id_vars="genre", var_name="feature", value_name="average")
sound["feature"] = sound["feature"].str.title()

fig = px.bar(sound, x="feature", y="average", color="genre", barmode="group",
             color_discrete_map=GENRE_COLORS, category_orders={"genre": GENRES},
             title="Average danceability, energy and valence (positivity) by genre",
             labels={"feature": "Audio feature", "average": "Average score (0-1)", "genre": "Genre"},
             height=420)
fig.update_layout(yaxis_range=[0, 1])
st.plotly_chart(fig, width="stretch")

st.caption(SOURCE_CAPTION + f" Source page: [{DATASET_NAME}]({SOURCE_URL}). "
           "The KPIs and all charts use the same filtered data.")

with st.expander("View the filtered data"):
    st.dataframe(filtered[["track_name", "track_artist", "genre", "subgenre", "release_year",
                           "track_popularity", "danceability", "energy", "valence"]],
                 hide_index=True)


# ----- Insights -----
st.subheader("Insights")

top = by_genre.iloc[0]
bottom = by_genre.iloc[-1]

col1, col2 = st.columns(2)
with col1:
    with card():
        st.markdown("##### :green[Q1] Newer is not always more popular")
        st.caption("With the default filters, songs from the 2000s have the lowest average popularity. "
                   "Recent releases and older classics both score higher.")
    with card():
        # This one changes with the filters
        st.markdown(f"##### :green[Q2] {top['genre']} leads this selection")
        st.caption(f"{top['genre']} has the highest median popularity ({top['median_popularity']:.0f}) "
                   f"and {bottom['genre']} has the lowest ({bottom['median_popularity']:.0f}).")
with col2:
    with card():
        st.markdown("##### :green[Q3] Pop subgenres lead, plus a surprise from Rock")
        st.caption("With the default filters, Pop subgenres like Post-Teen Pop (62) and Dance Pop (56) "
                   "are still near the top. The surprise is Permanent Wave in 2nd place (58), even "
                   "though it's a Rock subgenre and Rock overall is one of the least popular genres. "
                   "Permanent Wave is Spotify's label for alternative and new-wave rock bands whose "
                   "music has stayed popular, like The Smiths, The Cure, Depeche Mode, Radiohead "
                   "and Nirvana.")
    with card():
        st.markdown("##### :green[Q4] Each genre has its own sound")
        st.caption("EDM has the most energy, Rock is the least danceable, and Rap and Latin are "
                   "the most danceable, even where popularity is similar.")

with card():
    st.markdown("##### :orange[Limitations]")
    st.caption("Popularity is a single snapshot from January 2020, and genre comes from the playlist, "
               "not the song. The playlists lean toward recent, English and Spanish-language music. "
               "These are patterns in the data, not proof of cause and effect.")

footer()
