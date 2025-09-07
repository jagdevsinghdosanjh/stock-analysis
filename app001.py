import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("PLTR_stock_data.csv")
# st.write("Columns in your dataset:", df.columns.tolist())


# Title
st.title("PLTR Stock Analysis Dashboard")

# Show raw data
if st.checkbox("Show raw data"):
    st.write(df)

# Basic stats
st.subheader("Summary Statistics")
st.write(df.describe())

# Date range filter
df['date'] = pd.to_datetime(df['date'])
start_date = st.date_input("Start Date", df['date'].min())
end_date = st.date_input("End Date", df['date'].max())
filtered_df = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

# Plot closing price
st.subheader("Closing Price Over Time")
fig, ax = plt.subplots()
ax.plot(filtered_df['Date'], filtered_df['Close'], label='Close Price')
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.legend()
st.pyplot(fig)

# Moving Averages
st.subheader("Moving Averages")
for window in [20, 50, 100]:
    col_name = f"SMA_{window}"
    if col_name in df.columns:
        fig, ax = plt.subplots()
        ax.plot(filtered_df['date'], filtered_df['Close'], label='Close')
        ax.plot(filtered_df['date'], filtered_df[col_name], label=col_name)
        ax.set_title(f"{col_name} vs Close")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning(f"{col_name} not found in data.")

# Correlation heatmap
st.subheader("Correlation Heatmap")
fig, ax = plt.subplots()
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)
