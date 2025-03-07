import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#Helper function
def create_total_cnt_df(df):
    total_cnt_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum",
        "casual": "sum",
        "registered": "sum",
        "hum":"sum",
    }).reset_index()
    return total_cnt_df

def create_season_cnt_df(df):
    season_df = df.groupby(["season", "yr"])["cnt"].sum().reset_index()
    return season_df

def create_weekday_df(df):
    weekday_df = df.groupby(by="day_type")["cnt"].sum().reset_index()
    return weekday_df

def create_bining_df(df):
    bining_df = df[["cnt"]]
    max_cnt = df["cnt"].max()
    bins = [0, (1/3) * max_cnt, (2/3) * max_cnt, max_cnt]
    labels = ["Low", "Medium", "High"]
    bining_df["bins_category"] = pd.cut(bining_df["cnt"], bins=bins, labels=labels, include_lowest=True)
    bining_df = df["bins_category"].value_counts().reset_index()
    return bining_df

#Main function
day_df = pd.read_csv("all_data.csv")
day_df["dteday"] = pd.to_datetime(day_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

st.title('Bike Sharing Dashboard')
with st.sidebar:
    #Filter date
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

total_cnt_df = create_total_cnt_df(main_df)
season_df = create_season_cnt_df(main_df)
weekday_df = create_weekday_df(main_df)
bining_df = create_bining_df(main_df)

col1, col2, col3 = st.columns(3)
 #Total cnt
with col1:
    total_cnt = total_cnt_df.cnt.sum()
    st.metric("Jumlah Sewa", value=total_cnt)
 
 #Total casual
with col2:
    total_casual = total_cnt_df.casual.sum()
    st.metric("Jumlah Sewa Pengguna Casual", value=total_casual)
 
 #Total registered
with col3:
    total_registered = total_cnt_df.registered.sum()
    st.metric("Jumlah Sewa Pengguna Registered", value=total_registered)
    fig, ax = plt.subplots(figsize=(16, 8))

#Total cnt Visualization
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    total_cnt_df["dteday"],
    total_cnt_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

#Total 2011 and 2012 by Season
st.subheader("Jumlah Sewa Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="season", 
    y="cnt",
    hue="yr",
    data=season_df,
    ax=ax,
    palette=["#1F77B4", "#FF7F0E"]
)
ax.set_title("Jumlah Sewa Sepeda Berdasarkan Musim", fontsize=14)
ax.set_xlabel("Season (1=Spring, 2=Summer, 3=Fall, 4=Winter)")
ax.set_ylabel("Total Count")
ax.legend(title="Year")
st.pyplot(fig)

#Humidity vs Casual and Registered
st.subheader("Pengaruh Humidity Terhadap Jumlah Sewa Pengguna Casual dan Registered")
fig, ax = plt.subplots()
sns.scatterplot(
    x="hum", 
    y="casual", 
    data=total_cnt_df, 
    color="blue", 
    label="Casual", 
    alpha=0.5
)
sns.scatterplot(
    x="hum", 
    y="registered", 
    data=total_cnt_df, 
    color="orange", 
    label="Registered", 
    alpha=0.5
)
ax.set_xlabel("Humidity")
ax.set_ylabel("Total Count")
st.pyplot(fig)

#Bining and Manual Grouping
st.subheader("Analisis Lanjutan")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Distribusi Sewa Sepeda Weekend vs. Weekday")
    fig, ax = plt.subplots()
    ax.pie(
        weekday_df["cnt"], 
        labels=weekday_df["day_type"],
        autopct='%1.1f%%', 
        colors=["#72BCD4", "#D3D3D3"]
    )
    ax.set_title("Distribusi Sewa Sepeda Weekend vs. Weekday", fontsize=14)
    st.pyplot(fig)
 
with col2:
    st.subheader("Pengelompokan Berdasarkan Jumlah Sewa Harian")
    fig, ax = plt.subplots()
    sns.barplot(
        x="bins_category", 
        y="count", 
        data=bining_df.sort_values(by="count", ascending=False).head(5), 
        ci=None, 
        ax=ax,
        color="#72BCD4"
    )
    ax.set_title("Pengelompokan Berdasarkan Jumlah Sewa Harian", fontsize=14)
    ax.set_xlabel("Kategori")
    ax.set_ylabel("Jumlah Hari")
    st.pyplot(fig)
