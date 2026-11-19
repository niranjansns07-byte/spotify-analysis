import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Spotify Analysis", layout="wide")
st.markdown("""
<style>
/* Import elegant serif & clean sans-serif fonts */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Playfair+Display:wght@500;700&display=swap');

/* Main Page Subtle Royal Radial Gradient */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top right, #111D3B 0%, #060B19 75%);
}

/* Sidebar Styling with Gold Accent Border & Subtle Damask Pattern */
[data-testid="stSidebar"] {
    background-color: #0B132B;
    background-image: radial-gradient(rgba(212, 175, 55, 0.08) 1px, transparent 0);
    background-size: 20px 20px;
    border-right: 1.5px solid #D4AF37;
}

/* Royal Gold Headings */
h1, h2, h3 {
    font-family: 'Cinzel', 'Playfair Display', serif !important;
    color: #E5C158 !important;
    text-shadow: 0px 2px 6px rgba(0, 0, 0, 0.6);
    letter-spacing: 0.5px;
}

/* Metric Numbers & Labels */
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    color: #F8F5E6 !important;
}
[data-testid="stMetricLabel"] {
    color: #C5A059 !important;
    font-weight: 600;
}

/* Multiselect & Dropdown Gold Borders */
div[data-baseweb="select"] > div {
    border: 1px solid #D4AF37 !important;
    background-color: rgba(11, 19, 43, 0.85) !important;
    border-radius: 6px;
}

/* Selected Genre Pills (Royal Crimson with Gold Border) */
span[data-baseweb="tag"] {
    background-color: #7A1C24 !important;
    border: 1px solid #D4AF37 !important;
    color: #F8F5E6 !important;
}
</style>
""", unsafe_allow_html=True)
st.title("🎵 Spotify Music Trends & Audio Feature Analysis")

@st.cache_data
def load_data():
    return pd.read_csv("spotify_cleaned.csv")

df = load_data()

st.sidebar.header("Filters")
genres = st.sidebar.multiselect("Genre", sorted(df['track_genre'].unique()),
                                default=["pop", "rock", "hip-hop"])
pop_range = st.sidebar.slider("Popularity range", 0, 100, (0, 100))
feature = st.sidebar.selectbox("Audio feature",
    ['danceability','energy','valence','acousticness','speechiness','tempo','loudness'])

filtered = df[df['track_genre'].isin(genres) & df['popularity'].between(*pop_range)]

if filtered.empty:
    st.warning("No songs match these filters.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Songs", f"{len(filtered):,}")
c2.metric("Avg popularity", f"{filtered['popularity'].mean():.1f}")
c3.metric(f"Avg {feature}", f"{filtered[feature].mean():.2f}")

avg = filtered.groupby('track_genre')[feature].mean().reset_index()

fig_bar = px.bar(avg, x='track_genre', y=feature,
                 title=f"Average {feature} by genre")
fig_bar.update_traces(marker_color="#8B1E24")
fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_bar, width="stretch")

sample = filtered.sample(min(3000, len(filtered)), random_state=42)

fig_scatter = px.scatter(sample, x='valence', y='energy', color='track_genre',
                         hover_data=['track_name', 'artists'], opacity=0.6,
                         title="Valence vs Energy")
fig_scatter.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_scatter, width="stretch")

st.subheader("Most popular songs in selection")
st.dataframe(filtered.drop_duplicates('track_id')
             .sort_values('popularity', ascending=False)
             [['track_name','artists','track_genre','popularity']].head(20))