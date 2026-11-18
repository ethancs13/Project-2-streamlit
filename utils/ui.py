# Shared things every page uses: my info, the colors, the sidebar, and card styling.

import streamlit as st

NAME = "Ethan Sroka"
TAGLINE = "Data Science & Machine Learning Student, Metropolitan State University"
LINKEDIN = "https://www.linkedin.com/in/ethan-sroka-8402631a2/"
WEBSITE = "https://ethansroka.dev"
GITHUB_LAB = "https://github.com/ethancs13/gelkube-labs"
STATS_FU = "https://github.com/ethancs13/stats.fu"

# Spotify-style colors for the app
GREEN = "#1DB954"
LIGHT_GRAY = "#B3B3B3"
GRAY = "#6A6A6A"

# Colorblind-safe genre colors (checked against the dark background).
# Each genre always gets the same color on every chart.
GENRE_COLORS = {
    "EDM": "#3987e5",    # blue
    "Latin": "#d95926",  # orange
    "Pop": "#199e70",    # teal
    "R&B": "#c98500",    # yellow
    "Rap": "#d55181",    # pink
    "Rock": "#9085e9",   # violet
}
GENRES = list(GENRE_COLORS.keys())

SOURCE_CAPTION = ("Source: Spotify Songs dataset from TidyTuesday (2020-01-21), "
                  "collected with the spotifyr R package. 28,352 unique tracks.")

# A little CSS so containers made with card() look like Spotify's dark gray tiles
CSS = """
<style>
div[class*="st-key-card"] {
    background-color: #181818;
    padding: 1.1rem 1.2rem;
}
div[class*="st-key-hero"] {
    background: linear-gradient(135deg, #1a6b3a 0%, #121212 75%);
    padding: 2rem 2rem 1.5rem 2rem;
}
[data-testid="stMetric"] {
    background-color: #181818;
    border-radius: 12px;
    padding: 0.8rem 1rem;
}
[data-testid="stMetricValue"] {
    font-size: 1.75rem;
}
div[class*="st-key-profile"] img {
    border-radius: 50%;
    border: 3px solid #1DB954;
}
[data-baseweb="tag"] span {
    color: #000000;
}
/* Score bar card (used for danceability on the dashboard) */
.score-card {
    background-color: #181818;
    border-radius: 12px;
    padding: 0.8rem 1rem;
}
.score-label {
    font-size: 0.875rem;
}
.score-row {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0.9rem 0 0.75rem 0;
}
.score-bar {
    flex: 1;
    height: 16px;
    border-radius: 8px;
    /* Gray at 0, full Spotify green from 0.75 up (same colors as BAR_START, BAR_END, FULL_AT) */
    background: linear-gradient(90deg, #6a6a6a 0%, #1DB954 75%);
    position: relative;
    overflow: hidden;
}
.score-cover {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    background-color: #2a2a2a;
}
.score-end {
    font-size: 0.8rem;
    color: #B3B3B3;
}
.score-words {
    font-size: 0.875rem;
    font-weight: 600;
}
</style>
"""

card_count = 0


def card():
    # Returns a container with a dark gray background (styled by the CSS above).
    # Each card needs its own key, so a counter is added to the name.
    global card_count  # pylint: disable=global-statement
    card_count += 1
    return st.container(border=True, key=f"card_{card_count}")


def setup_page(title):
    # Page settings, the CSS, and the sidebar with my name and links
    global card_count  # pylint: disable=global-statement
    card_count = 0
    st.set_page_config(page_title=title + " | " + NAME, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    st.sidebar.markdown(f"### :green[{NAME}]")
    st.sidebar.caption(TAGLINE)
    st.sidebar.markdown(f"[LinkedIn]({LINKEDIN}) | [ethansroka.dev]({WEBSITE})")
    st.sidebar.divider()


def page_header(title, subtitle):
    # Big title with a short gray subtitle under it
    st.title(title)
    st.caption(subtitle)


# Colors for the score bar (these must match the gradient in the CSS above)
BAR_START = (106, 106, 106)  # #6a6a6a gray
BAR_END = (29, 185, 84)      # #1DB954 Spotify green
FULL_AT = 0.75               # the bar is fully green from 0.75 to 1


def bar_color(score):
    # Works out the bar's color at this score, so the words under it can match.
    # t goes from 0 (all gray) to 1 (all green).
    t = min(score / FULL_AT, 1)
    red = round(BAR_START[0] + (BAR_END[0] - BAR_START[0]) * t)
    green = round(BAR_START[1] + (BAR_END[1] - BAR_START[1]) * t)
    blue = round(BAR_START[2] + (BAR_END[2] - BAR_START[2]) * t)
    return f"#{red:02x}{green:02x}{blue:02x}"


def score_bar(label, score, words, help_text):
    # A KPI card like st.metric, but with a 0 to 1 bar instead of a number.
    # The bar is a gray-to-green gradient, and a dark gray cover hides the part above the score.
    # Hovering the card shows help_text.
    cover = 100 - round(score * 100)
    html = (
        f'<div class="score-card" title="{help_text}">'
        f'<div class="score-label">{label}</div>'
        f'<div class="score-row">'
        f'<span class="score-end">0</span>'
        f'<div class="score-bar"><div class="score-cover" style="width: {cover}%"></div></div>'
        f'<span class="score-end">1</span>'
        f'</div>'
        f'<div class="score-words" style="color: {bar_color(score)}">{words}</div>'
        f'</div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def footer():
    st.divider()
    st.caption(f"2026 {NAME} | [LinkedIn]({LINKEDIN}) | [ethansroka.dev]({WEBSITE}) | "
               "Built with Streamlit, pandas and Plotly")


def how_to_read(points):
    # Card with the "How to read this chart" bullets
    with card():
        st.markdown("##### :green[How to read this chart]")
        for p in points:
            st.markdown("- " + p)


def observations(points):
    # Card with what I noticed in the chart
    with card():
        st.markdown("##### :green[Observations]")
        for p in points:
            st.markdown("- " + p)


def question(text):
    # Small green label with the question a chart answers
    st.markdown(f":green-badge[Question] **{text}**")
