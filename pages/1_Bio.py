# Bio page: professional summary, highlights, and my visualization philosophy.

import os

import streamlit as st

from utils.ui import (GITHUB_LAB, LINKEDIN, NAME, TAGLINE, WEBSITE, card, footer,
                      page_header, setup_page)

setup_page("Bio")

PHOTO = os.path.join(os.path.dirname(__file__), "..", "assets", "profile.jpg")

page_header("Professional Bio", "About me, what I work with, and how I approach data visualization")

left, right = st.columns([1, 2.4], gap="large")

# ----- Profile card -----
with left:
    with card():
        # Only show the photo if I've added it to the assets folder
        if os.path.exists(PHOTO):
            # The photo is 150x150, so show it at that size so it doesn't look blurry.
            # The "profile" key lets the CSS make it round.
            # alt is the text screen readers read out for the image
            with st.container(key="profile"):
                st.image(PHOTO, width=150,
                         caption="Ethan Sroka, DSML student at Metropolitan State University",
                         alt="Headshot of Ethan Sroka smiling, wearing glasses and a cream knit "
                             "sweater, in front of a light gray background.")
        else:
            st.info("Profile photo coming soon.")
        st.markdown(f"### {NAME}")
        st.caption(TAGLINE)
        st.link_button("LinkedIn", LINKEDIN, width="stretch")
        st.link_button("ethansroka.dev", WEBSITE, width="stretch")
        st.link_button("Home lab on GitHub", GITHUB_LAB, width="stretch")

# ----- Summary and highlights -----
with right:
    with card():
        st.markdown("#### :green[Summary]")
        st.write(
            "I'm a Data Science and Machine Learning student at Metropolitan State University. "
            "I like turning messy, real-world data into clear answers people can act on. "
            "I use Python, pandas and Plotly for analysis and Streamlit to turn it into apps, "
            "and my full-stack background lets me build the product around the data. "
            "Right now I'm focused on machine learning and on deploying ML systems with Kubernetes."
        )

    st.markdown("#### :green[Highlights]")
    col1, col2 = st.columns(2)
    with col1:
        with card():
            st.markdown("**Coursework**")
            st.caption("DSML program at Metro State: data visualization, statistics and machine learning.")
        with card():
            st.markdown("**Full-stack apps**")
            st.caption("React, Node.js / Express, MongoDB and Flutter.")
    with col2:
        with card():
            st.markdown("**Data tools**")
            st.caption("Python, pandas, NumPy, Plotly, Streamlit and Jupyter.")
        with card():
            st.markdown("**Kubernetes home lab**")
            st.caption("Building clusters with tools I learned about at KubeCon.")

    with card():
        st.markdown("**Toolbox**")
        st.markdown(
            ":green-badge[Python] :green-badge[pandas] :green-badge[Plotly] :green-badge[Streamlit] "
            ":gray-badge[Git] :gray-badge[React] :gray-badge[Node.js] :gray-badge[Express] "
            ":gray-badge[MongoDB] :gray-badge[Flutter] :gray-badge[npm] :blue-badge[Kubernetes]"
        )

# ----- Visualization philosophy -----
st.write("")
st.markdown("#### :green[My visualization philosophy]")
col1, col2, col3 = st.columns(3)
with col1:
    with card():
        st.markdown("**Clarity first**")
        st.caption("Every chart answers one question, with a plain title and labeled axes and units.")
with col2:
    with card():
        st.markdown("**Accessible by default**")
        st.caption("Colorblind-safe colors and high contrast. Color is never the only way "
                   "to tell things apart.")
with col3:
    with card():
        st.markdown("**Honest and ethical**")
        st.caption("Bars start at zero, scales aren't stretched, and I describe patterns "
                   "without claiming causes.")

footer()
