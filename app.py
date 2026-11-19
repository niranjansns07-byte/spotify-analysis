import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Spotify Analysis", layout="wide")
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
st.plotly_chart(px.bar(avg, x='track_genre', y=feature,
                title=f"Average {feature} by genre"), use_container_width=True)

sample = filtered.sample(min(3000, len(filtered)), random_state=42)
st.plotly_chart(px.scatter(sample, x='valence', y='energy', color='track_genre',
                hover_data=['track_name', 'artists'], opacity=0.6,
                title="Valence vs Energy"), use_container_width=True)

st.subheader("Most popular songs in selection")
st.dataframe(filtered.drop_duplicates('track_id')
             .sort_values('popularity', ascending=False)
             [['track_name','artists','track_genre','popularity']].head(20))