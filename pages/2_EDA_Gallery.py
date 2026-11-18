# EDA Gallery: five different chart types, each one answers a question about the data.
# Each chart is in its own tab. Under each chart: "How to read" on the left, observations on the right.

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data import load_data
from utils.ui import (GENRE_COLORS, GENRES, GRAY, GREEN, LIGHT_GRAY, SOURCE_CAPTION, footer,
                      how_to_read, observations, page_header, question, setup_page)

setup_page("EDA Gallery")
df = load_data()

page_header("EDA Gallery",
            "Six charts, six questions. Hover for exact values, drag to zoom, double-click to reset.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Genre Trends", "Heatmap"]
)


# ----- Chart 1: Histogram -----
with tab1:
    question("Are most tracks hits, or is popularity concentrated in a few songs?")

    choice = st.selectbox("Show genre", ["All genres"] + GENRES)
    if choice == "All genres":
        hist_data = df
        color = GREEN
    else:
        hist_data = df[df["genre"] == choice]
        color = GENRE_COLORS[choice]

    fig = px.histogram(
        hist_data,
        x="track_popularity",
        color_discrete_sequence=[color],
        title=f"Distribution of track popularity - {choice} ({len(hist_data):,} tracks)",
        labels={"track_popularity": "Track popularity (0-100)"},
    )
    fig.update_traces(xbins=dict(start=0, end=101, size=5), marker_line_color="#121212",
                      marker_line_width=1)
    fig.update_layout(yaxis_title="Number of tracks")

    # Mark the median and point out the big spike at 0
    median = hist_data["track_popularity"].median()
    fig.add_vline(x=median, line_dash="dash", line_color=LIGHT_GRAY,
                  annotation_text=f"Median = {median:.0f}")
    zero_count = (hist_data["track_popularity"] == 0).sum()
    first_bar = (hist_data["track_popularity"] < 5).sum()
    fig.add_annotation(x=2.5, y=first_bar, text=f"{zero_count:,} tracks have a score of 0",
                       ax=80, ay=-30)

    st.plotly_chart(fig, width="stretch")
    st.caption(SOURCE_CAPTION)

    left, right = st.columns(2)
    with left:
        how_to_read([
            "Each bar covers 5 points of popularity (0-4, 5-9, and so on). The height is the number of tracks.",
            "The dashed line is the median. Half the tracks are below it, half above.",
            "Use the dropdown to compare one genre with all tracks.",
        ])
    with right:
        observations([
            "Most tracks are in the middle (21 to 58), and the median is 42.",
            "Big spike at 0: 2,616 tracks (about 9%) score 0. These might be tracks with very few "
            "plays or tracks that were removed.",
            "Real hits are rare. Less than 2% of tracks score 80 or higher.",
            "EDM has the most zero-popularity tracks (13%), and Pop has the fewest (6%).",
        ])


# ----- Chart 2: Box plot -----
with tab2:
    metric_names = {
        "track_popularity": "Popularity (0-100)",
        "energy": "Energy (0-1)",
        "danceability": "Danceability (0-1)",
        "valence": "Valence / positivity (0-1)",
        "tempo": "Tempo (beats per minute)",
        "duration_min": "Duration (minutes)",
    }
    question("How do the genres compare with each other?")
    metric = st.radio("Pick a measure", list(metric_names.keys()),
                      format_func=lambda m: metric_names[m], horizontal=True)

    # Sort genres from highest median to lowest
    order = df.groupby("genre")[metric].median().sort_values(ascending=False).index.tolist()

    fig = px.box(
        df,
        x="genre",
        y=metric,
        color="genre",
        color_discrete_map=GENRE_COLORS,
        category_orders={"genre": order},
        points=False,
        title=f"{metric_names[metric]} by playlist genre (sorted by median)",
        labels={"genre": "Playlist genre", metric: metric_names[metric]},
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, width="stretch")
    st.caption(SOURCE_CAPTION)

    left, right = st.columns(2)
    with left:
        how_to_read([
            "Each box holds the middle 50% of tracks in a genre. The line inside is the median.",
            "Whiskers show the usual range. Genre names are on the x-axis, so color isn't needed.",
            "Genres are sorted from highest median (left) to lowest (right).",
        ])
    with right:
        observations([
            "Popularity: Pop has the highest median (50) and EDM has the lowest (33).",
            "The boxes overlap a lot, so genre alone doesn't decide popularity.",
            "Energy: EDM is the highest (0.84) and R&B the lowest (0.59).",
            "Danceability: Rap and Latin are the highest (about 0.73), and Rock is the lowest (0.52).",
        ])
    with st.expander("View this data as a table"):
        st.dataframe(df.groupby("genre")[metric].describe().round(2))


# ----- Chart 3: Scatter plot -----
with tab3:
    question("Do energy and danceability have anything to do with loudness or tempo (BPM)?")

    x_names = {"energy": "Energy (0-1)", "danceability": "Danceability (0-1)"}
    y_names = {"loudness": "Loudness (dB, closer to 0 = louder)", "tempo": "Tempo (beats per minute)"}

    col1, col2, col3 = st.columns(3)
    x = col1.selectbox("X-axis", list(x_names.keys()), format_func=lambda c: x_names[c])
    y = col2.selectbox("Y-axis", list(y_names.keys()), format_func=lambda c: y_names[c])
    highlight = col3.selectbox("Highlight a genre", ["All genres"] + GENRES)

    if highlight == "All genres":
        # Every track colored by its own genre
        scatter_data = df.assign(group=df["genre"])
        colors = GENRE_COLORS
        order = {"group": GENRES}
        r = df[x].corr(df[y])
        title_end = "all genres"
    else:
        # Color the chosen genre and make every other genre gray.
        # The chosen genre goes last so its dots are drawn on top.
        others = df[df["genre"] != highlight].assign(group="Other genres")
        chosen = df[df["genre"] == highlight].assign(group=highlight)
        scatter_data = pd.concat([others, chosen])
        colors = {highlight: GENRE_COLORS[highlight], "Other genres": GRAY}
        order = {}
        r = chosen[x].corr(chosen[y])
        title_end = highlight + " highlighted"

    x_label = x_names[x].split(" (")[0]
    y_label = y_names[y].split(" (")[0]

    fig = px.scatter(
        scatter_data,
        x=x,
        y=y,
        color="group",
        color_discrete_map=colors,
        category_orders=order,
        opacity=0.5,
        hover_name="track_name",
        hover_data={"track_artist": True, "genre": True, "group": False},
        title=f"{x_label} vs. {y_label} - {title_end} (correlation r = {r:.2f})",
        labels={x: x_names[x], y: y_names[y], "group": "", "track_artist": "Artist",
                "genre": "Genre"},
        render_mode="webgl",
        height=520,
    )

    # Point out the quietest track (only makes sense on the loudness chart)
    if y == "loudness":
        quietest = df.loc[df["loudness"].idxmin()]
        fig.add_annotation(x=quietest[x], y=quietest["loudness"], ax=120, ay=-10,
                           text=f"Quietest track: {quietest['track_name']} (nature sounds)")

    st.plotly_chart(fig, width="stretch")
    st.caption(SOURCE_CAPTION)

    left, right = st.columns(2)
    with left:
        how_to_read([
            "Each dot is one track. Pick what goes on each axis with the dropdowns. Loudness is in "
            "negative decibels, so -5 dB is louder than -15 dB.",
            "\"All genres\" colors every track by genre (click a genre in the legend to hide it). "
            "Pick one genre to show it in color with the rest in gray.",
            "The r in the title is the correlation. Close to 0 means no straight-line relationship, "
            "and close to 1 or -1 means a strong one.",
        ])
    with right:
        observations([
            "Energy and loudness are strongly related (r = 0.68). This is the only strong pair of the four.",
            "Danceability and loudness have almost no relationship (r = 0.02).",
            "Tempo barely relates to energy (r = 0.15) or danceability (r = -0.18). "
            "Most songs sit between 100 and 134 BPM no matter how energetic they are.",
            "Danceability peaks at medium tempos: the median is 0.72 for 90-110 BPM, but only "
            "0.58 above 150 BPM.",
            "The quietest outliers (loudness view) are nature or ambient tracks, like \"Peaceful Forest\" at -46 dB.",
        ])


# ----- Chart 4: Line chart -----
with tab4:
    question("Has the sound of music changed over time?")

    feature_names = {
        "valence": "Valence (positivity)",
        "danceability": "Danceability",
        "energy": "Energy",
        "acousticness": "Acousticness",
    }
    picked = st.multiselect("Features to show (all are on a 0-1 scale)", list(feature_names.keys()),
                            default=["valence", "acousticness"],
                            format_func=lambda f: feature_names[f])

    # Median of each feature per year. Skip years before 1970 and years with under 30 tracks.
    yearly = df.groupby("release_year")[list(feature_names.keys())].median()
    yearly["tracks"] = df.groupby("release_year").size()
    yearly = yearly[(yearly.index >= 1970) & (yearly["tracks"] >= 30)].reset_index()

    if picked:
        # px.line needs "long" data: one row per year per feature
        long_data = yearly.melt(id_vars=["release_year", "tracks"], value_vars=picked,
                                var_name="feature", value_name="median")
        long_data["feature"] = long_data["feature"].map(feature_names)

        fig = px.line(
            long_data,
            x="release_year",
            y="median",
            color="feature",
            color_discrete_sequence=["#3987e5", "#d95926", "#199e70", "#c98500"],
            hover_data={"tracks": True},
            title="Median audio features by album release year (years with 30+ tracks)",
            labels={"release_year": "Album release year", "median": "Median score (0-1)",
                    "feature": "Feature", "tracks": "Tracks that year"},
        )
        fig.update_layout(yaxis_range=[0, 1])
        st.plotly_chart(fig, width="stretch")
    else:
        st.info("Pick at least one feature to show the chart.")
    st.caption(SOURCE_CAPTION + " Years before 1970 are left out because they have very few tracks.")

    left, right = st.columns(2)
    with left:
        how_to_read([
            "The x-axis is the year the album came out. Each line is one feature's median that year.",
            "All features use the same 0-1 scale, so the lines can be compared directly.",
            "Hover to see how many tracks are behind each point.",
        ])
    with right:
        observations([
            "Valence (positivity) dropped from about 0.62 (1980s-2000s) to about 0.44 around 2015.",
            "Acousticness fell from about 0.23 in 1975 to about 0.06 in the 2000s and 2010s.",
            "Danceability rose from about 0.51 in 1975 to around 0.65-0.70 recently.",
            "Over 70% of tracks are from 2010 or later. Older years are mostly well-known classics.",
        ])


# ----- Chart 5: Genre trends (line chart + bar chart) -----
with tab5:
    question("How has each genre's popularity changed over time, and which genres are most popular now?")

    # Group release years into 5-year periods. 2020 only has January, so it joins 2015-2019.
    trend = df[df["release_year"] >= 1980].copy()
    trend["period"] = (trend["release_year"] // 5 * 5).clip(upper=2015)
    trend = trend.groupby(["period", "genre"]).agg(
        median_popularity=("track_popularity", "median"),
        tracks=("track_id", "count"),
    ).reset_index()
    # Skip points with fewer than 30 tracks because they are too noisy
    trend = trend[trend["tracks"] >= 30]
    trend["period_label"] = trend["period"].astype(str) + "-" + (trend["period"] + 4).astype(str)
    trend.loc[trend["period"] == 2015, "period_label"] = "2015-2020"

    fig = px.line(
        trend,
        x="period",
        y="median_popularity",
        color="genre",
        color_discrete_map=GENRE_COLORS,
        category_orders={"genre": GENRES},
        markers=True,
        hover_data={"period": False, "period_label": True, "tracks": True},
        title="Median popularity (in 2020) of songs released in each 5-year period, by genre",
        labels={"period": "Album release period (start year)",
                "median_popularity": "Median popularity (0-100)", "genre": "Genre",
                "period_label": "Released", "tracks": "Tracks"},
    )
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, width="stretch")

    # Most popular now: only songs released in 2019 or 2020
    recent = df[df["release_year"] >= 2019].groupby("genre").agg(
        median_popularity=("track_popularity", "median"),
        tracks=("track_id", "count"),
    ).reset_index().sort_values("median_popularity", ascending=False)

    fig = px.bar(
        recent,
        x="genre",
        y="median_popularity",
        color="genre",
        color_discrete_map=GENRE_COLORS,
        text="median_popularity",
        hover_data={"tracks": True},
        title="Most popular genres now: median popularity of songs released in 2019-2020",
        labels={"genre": "Playlist genre", "median_popularity": "Median popularity (0-100)",
                "tracks": "Tracks"},
        height=380,
    )
    fig.update_traces(texttemplate="%{text:.0f}", textposition="outside")
    fig.update_layout(showlegend=False, yaxis_range=[0, 100])
    st.plotly_chart(fig, width="stretch")
    st.caption(SOURCE_CAPTION + " Only periods with 30+ tracks in a genre are shown.")

    left, right = st.columns(2)
    with left:
        how_to_read([
            "Top chart: each line is a genre. Each point is the median popularity of that genre's songs "
            "released in a 5-year period. Click a genre in the legend to hide it.",
            "Bottom chart: the same measure, but only for songs released in 2019-2020.",
            "Important: popularity was measured once, in January 2020. The lines show how popular "
            "older songs still were in 2020, not how popular they were when they came out.",
        ])
    with right:
        observations([
            "Most popular now: Rap (54), Pop (53) and R&B (51) lead among 2019-2020 releases. "
            "EDM (38) and Rock (37) are clearly lower.",
            "Most genres dip for songs from 2005-2014. R&B fell to 18.5 for 2005-2009 releases, and "
            "then 2015-2020 releases rose back to 47.",
            "Rock is the opposite of the other genres. Its older songs (1980-2004) score about 50-53, "
            "but its newer songs only score about 36-37.",
            "Pop stays near the top in almost every period (about 49-53).",
            "EDM only has enough tracks from 2005 on, and its 2005-2009 songs have a median of just 5.",
        ])


# ----- Chart 6: Heatmap -----
with tab6:
    question("Which audio features go together, and do any go with popularity?")

    columns = {
        "track_popularity": "Popularity", "danceability": "Danceability", "energy": "Energy",
        "loudness": "Loudness", "speechiness": "Speechiness", "acousticness": "Acousticness",
        "instrumentalness": "Instrumentalness", "liveness": "Liveness", "valence": "Valence",
        "tempo": "Tempo", "duration_min": "Duration",
    }
    corr = df[list(columns.keys())].corr().rename(index=columns, columns=columns)

    # Blue = negative, dark gray = none, red = positive (colorblind-safe)
    fig = px.imshow(
        corr,
        text_auto=".2f",
        zmin=-1,
        zmax=1,
        color_continuous_scale=[[0, "#3987e5"], [0.5, "#383835"], [1, "#e66767"]],
        title="Correlation between audio features (Pearson r)",
        aspect="auto",
        height=600,
    )
    st.plotly_chart(fig, width="stretch")
    st.caption(SOURCE_CAPTION)

    left, right = st.columns(2)
    with left:
        how_to_read([
            "Each square is the correlation (r) between the row and column, from -1 to +1.",
            "Red = both go up together, blue = one goes up as the other goes down, gray = no relationship.",
            "The diagonal is always 1.00 because each feature matches itself.",
        ])
    with right:
        observations([
            "Strongest pairs: energy and loudness (+0.68), energy and acousticness (-0.55).",
            "Danceability and valence are somewhat related (+0.33).",
            "Popularity is only weakly related to every feature (all between -0.15 and +0.15). "
            "The sound of a song alone doesn't explain popularity.",
            "Correlation does not prove cause and effect.",
        ])

footer()
