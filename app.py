import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and clean data
df = pd.read_csv("data/PLTR_stock_data.csv")
df.columns = df.columns.str.strip().str.lower()  # Clean column names

# Display column names for debugging
st.write("Available columns:", df.columns.tolist())

# Title
st.title("📈 PLTR Stock Analysis Dashboard")

# Show raw data
if st.checkbox("Show raw data"):
    st.write(df)

# Basic stats
st.subheader("📊 Summary Statistics")
st.write(df.describe())

# Convert date column
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])
else:
    st.error("❌ 'date' column not found in dataset.")
    st.stop()

# Date range filter
start_date = st.date_input("Start Date", df['date'].min())
end_date = st.date_input("End Date", df['date'].max())
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Plot closing price
if 'close' in df.columns:
    st.subheader("📉 Closing Price Over Time")
    fig, ax = plt.subplots()
    ax.plot(filtered_df['date'], filtered_df['close'], label='Close Price', color='blue')
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("⚠️ 'close' column not found in data.")

# Moving Averages
st.subheader("📈 Moving Averages")
for window in [20, 50, 100]:
    col_name = f"sma_{window}"
    if col_name in df.columns:
        fig, ax = plt.subplots()
        ax.plot(filtered_df['date'], filtered_df['close'], label='Close', color='gray')
        ax.plot(filtered_df['date'], filtered_df[col_name], label=col_name.upper(), linestyle='--')
        ax.set_title(f"{col_name.upper()} vs Close")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning(f"⚠️ {col_name.upper()} not found in data.")

# Correlation heatmap
st.subheader("🔍 Correlation Heatmap")
fig, ax = plt.subplots()
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)
