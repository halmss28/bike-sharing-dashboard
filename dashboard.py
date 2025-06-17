import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Bike Sharing", layout="wide")
st.title("📊 Dashboard Analisis Peminjaman Sepeda")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv", parse_dates=["dteday"])
    season_map = {1: 'Semi', 2: 'Panas', 3: 'Gugur', 4: 'Dingin'}
    df['Musim'] = df['season'].map(season_map)
    return df

data = load_data()

# Sidebar Filter
st.sidebar.header("Filter")
musim = st.sidebar.multiselect(
    "Pilih Musim",
    options=data["Musim"].unique(),
    default=data["Musim"].unique()
)

# Filter data sesuai musim
filtered_data = data[data["Musim"].isin(musim)]

# Grafik Tren Harian
st.subheader("Tren Jumlah Peminjaman Sepeda per Hari")
fig1, ax1 = plt.subplots(figsize=(14, 5))
sns.lineplot(data=filtered_data, x="dteday", y="cnt", ax=ax1, color='dodgerblue')
ax1.set_xlabel("Tanggal")
ax1.set_ylabel("Jumlah Peminjaman")
st.pyplot(fig1)

# Grafik Rata-Rata Musim
st.subheader("Rata-Rata Peminjaman per Musim")
fig2, ax2 = plt.subplots(figsize=(6, 4))
avg_per_season = data.groupby("Musim")["cnt"].mean().reindex(['Semi', 'Panas', 'Gugur', 'Dingin'])
sns.barplot(x=avg_per_season.index, y=avg_per_season.values, ax=ax2, palette="viridis")
ax2.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig2)

# Insight Ringkas
st.markdown("### 🔍 Insight")
st.markdown("""
- **Musim panas dan gugur** menunjukkan volume peminjaman sepeda tertinggi.
- Terdapat tren musiman yang cukup jelas, dengan fluktuasi peminjaman harian yang signifikan.
""")
