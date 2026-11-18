# Project 2, Part 1: Asking Better Questions with Data

**Ethan Sroka** | Data Science & Machine Learning, Metropolitan State University | November 18, 2026

## Step 1: Dataset

| | |
|---|---|
| **Dataset name** | Spotify Songs (TidyTuesday, week of 2020-01-21) |
| **Source link** | https://github.com/rfordatascience/tidytuesday/tree/master/data/2020/2020-01-21 |
| **Number of rows** | 32,833 rows (28,352 unique tracks after removing duplicates), 23 columns |

**Description:** This dataset contains about 33,000 songs taken from Spotify playlists in six genres: EDM, Latin, Pop, R&B, Rap and Rock. Kaylin Pavlik collected it from the Spotify Web API using the `spotifyr` R package, and it was shared through the TidyTuesday project. Each row includes the track, artist, album release date, playlist genre and subgenre, Spotify's 0-100 popularity score, and audio features such as danceability, energy, valence (positivity), loudness, tempo and duration.

## Step 2: The 5E Data Questioning Cycle

### Engage: My initial questions

1. How are features like acousticness, loudness, energy and popularity correlated with each other?
2. How has the popularity of different genres changed over time, and which genres are the most popular now?
3. Do energy and danceability have anything to do with loudness or tempo (BPM)?

### Explore: Using generative AI to expand my questions

**AI tool:** Claude (Anthropic)

**Exact prompt I used:**

> I'm working on a data visualization project using the TidyTuesday "Spotify Songs" dataset (32,833 rows). The columns are: track name, artist, track popularity (0-100), album release date, playlist genre (edm, latin, pop, r&b, rap, rock), playlist subgenre, danceability, energy, key, loudness, mode (major/minor), speechiness, acousticness, instrumentalness, liveness, valence, tempo, and duration. My own starting questions are: (1) how are features like acousticness, loudness, energy and popularity correlated, (2) how has the popularity of different genres changed over time and which are most popular now, and (3) do energy and danceability have anything to do with loudness or tempo. Suggest 10 more questions I could answer with visualizations that are different from mine, from simple comparisons to trends over time. Include questions I probably wouldn't think of.

**AI-generated questions:**

1. How is track popularity distributed? Are hits rare, and why do so many tracks have a popularity of exactly 0?
2. How do the six genres differ in their typical energy, danceability and valence (their overall "sound profile")?
3. Has the emotional tone of music (valence, or how positive it sounds) changed across release years?
4. Which subgenres are much more or less popular than their main genre?
5. Do songs in a major key differ from songs in a minor key in popularity or valence?
6. Have songs gotten shorter over time, and are shorter songs more popular?
7. Is there a tempo "sweet spot" where popular songs cluster?
8. Which artists show up in the most playlists, or across more than one genre?
9. Are tracks with lots of spoken words (speechiness) concentrated in certain genres?
10. Do mostly instrumental tracks have lower popularity than tracks with vocals?

### Explain: Four selected questions and why they matter

| # | Question | Source | Why it matters |
|---|---|---|---|
| A | How has the popularity of different genres changed over time, and which genres are the most popular now? | Mine | Genres go in and out of style, and knowing which ones lead today is useful for artists, playlist curators and listeners. It also made me think carefully about the data: popularity was measured once (January 2020), so I can only compare how popular songs from different release years still are, not how a genre's popularity rose and fell. |
| B | Do energy and danceability have anything to do with loudness or tempo (BPM)? | Mine | It's easy to assume a fast or loud song is automatically energetic or danceable. Testing this tells me which audio features carry the same information and which really measure something different, which matters before using them in any model. |
| C | How is track popularity distributed? Are hits rare, and why do so many tracks score exactly 0? | AI | Every other popularity question depends on this one. If the distribution is skewed or has a strange spike, averages can be misleading. It also points out a data quality issue I need to explain before drawing conclusions. |
| D | Has the emotional tone of music (valence) changed across release years? | AI | This turns the dataset into a story about how music has changed. It is also a good companion to my genre-over-time question, since it looks at change in the sound itself instead of in popularity. |

### Elaborate: Visualization type for each question

| # | Visualization | Justification |
|---|---|---|
| A | **Multi-line chart** of median popularity by 5-year release period for each genre, plus a **bar chart** of median popularity for 2019-2020 releases | A line per genre on a shared time axis makes it easy to compare trends, and grouping years into 5-year periods smooths out years with only a few songs. The bar chart answers "most popular now" directly. Its y-axis starts at zero so the gaps between genres aren't exaggerated. |
| B | **Scatter plot** with dropdowns to put energy or danceability on the x-axis and loudness or tempo on the y-axis | These are all continuous variables, so a scatter plot shows the direction and strength of each relationship. The correlation (r) is shown in the title, hover tooltips identify outliers, and you can highlight one genre while the rest stay gray. |
| C | **Histogram** of popularity in 5-point bins, with a median line | A histogram shows the shape of the distribution: where most songs sit, how rare hits are, and the unusual spike at 0. A genre dropdown lets you compare each genre with the overall shape. |
| D | **Line chart** of median valence (and other features) by release year | Change over time is best shown on a time axis. I use medians because they aren't pulled by extreme values, and I only include years with at least 30 tracks. |

My first question (correlations between acousticness, loudness, energy and popularity) is answered by a **correlation heatmap** in the EDA Gallery. It shows every pair at once with a colorblind-safe blue-gray-red scale and the exact r value in each cell.

### Evaluate: Reflection

The AI suggested questions I hadn't thought of, especially the spike of tracks with exactly zero popularity and whether the emotional tone of music has changed over time. My own questions were mostly about relationships between audio features and about genres. The AI pushed my analysis toward data quality and the bigger story of how music has changed. Working through my genre-over-time question with AI also made me realize the popularity score is a single snapshot, so I changed how I phrase my conclusions. Overall, the AI broadened what I looked at, but I still chose which questions to pursue based on what I was most curious about.
