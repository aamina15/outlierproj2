import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Price Outlier Detection",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Price Outlier Detection using Percentiles")

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    # Load dataset
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Check if price column exists
    if "price" not in df.columns:
        st.error("The uploaded dataset does not contain a 'price' column.")
        st.stop()

    # Statistics before cleaning
    st.subheader("Price Statistics (Before Cleaning)")
    st.dataframe(df["price"].describe())

    # Percentile thresholds
    min_threshold, max_threshold = df["price"].quantile([0.01, 0.999])

    st.subheader("Outlier Thresholds")

    col1, col2 = st.columns(2)

    col1.metric("1st Percentile", f"{min_threshold:.2f}")
    col2.metric("99.9th Percentile", f"{max_threshold:.2f}")

    # Remove outliers
    df2 = df[
        (df["price"] > min_threshold) &
        (df["price"] < max_threshold)
    ]

    st.success(f"Rows Before Cleaning: {df.shape[0]}")
    st.success(f"Rows After Cleaning: {df2.shape[0]}")

    # Statistics after cleaning
    st.subheader("Price Statistics (After Cleaning)")
    st.dataframe(df2["price"].describe())

    # Histograms
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Before Cleaning")
        fig, ax = plt.subplots()
        ax.hist(df["price"], bins=40)
        ax.set_xlabel("Price")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    with col2:
        st.subheader("After Cleaning")
        fig, ax = plt.subplots()
        ax.hist(df2["price"], bins=40)
        ax.set_xlabel("Price")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    # Download cleaned dataset
    csv = df2.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Cleaned Dataset",
        csv,
        "cleaned_data.csv",
        "text/csv"
    )

else:
    st.info("Please upload a CSV file to begin.")
