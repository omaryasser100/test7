
import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page config
# -----------------------
st.set_page_config(
    page_title="Melbourne Housing Dashboard",
    layout="wide"
)

# -----------------------
# Load data
# -----------------------
@st.cache_data
def load_data():
    return pd.read_csv("final_df.csv")

df = load_data()

# -----------------------
# Title
# -----------------------
st.title("🏠 Melbourne Housing Dashboard")

# -----------------------
# Sidebar navigation
# -----------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Data Overview",
        "Univariate Analysis",
        "Bivariate Analysis",
        "Correlation Heatmap",
        "Summary"
    ]
)

# ==================================================
# PAGE 1: DATA OVERVIEW
# ==================================================
if page == "Data Overview":

    st.subheader("📊 Dataset Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Listings", len(df))
    col2.metric("Average Price", round(df['Price'].mean(), 2))
    col3.metric("Median Price", round(df['Price'].median(), 2))
    col4.metric("Avg. CBD Distance (km)", round(df['CBD_Distance'].mean(), 2))

    st.markdown("---")

    st.subheader("🔍 Sample of the Data")
    st.dataframe(df.head())

# ==================================================
# PAGE 2: UNIVARIATE ANALYSIS
# ==================================================
elif page == "Univariate Analysis":

    st.subheader("📈 Univariate Analysis")

    feature = st.selectbox(
        "Select a feature",
        [
            "Price",
            "Rooms",
            "Landsize",
            "Distance",
            "CBD_Distance",
        ]
    )

    fig = px.histogram(
        df,
        x=feature,
        title=f"Distribution of {feature}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# PAGE 3: BIVARIATE ANALYSIS
# ==================================================
elif page == "Bivariate Analysis":

    st.subheader("📊 Bivariate Analysis")

    analysis_type = st.selectbox(
        "Select Analysis",
        [
            "Price vs CBD Distance",
            "Price by Rooms",
            "Price by Property Type",
            "Price by Parking Ratio",
            "Price vs Price Per Land"
        ]
    )

    if analysis_type == "Price vs CBD Distance":
        fig = px.scatter(df, x="CBD_Distance", y="Price")

    elif analysis_type == "Price by Rooms":
        fig = px.box(df, x="Rooms", y="Price")

    elif analysis_type == "Price by Property Type":
        fig = px.box(df, x="Type", y="Price")

    elif analysis_type == "Price by Parking Ratio":
        fig = px.box(df, x="ParkingRatio", y="Price")

    else:
        fig = px.scatter(df, x="PricePerLand", y="Price")

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# PAGE 4: CORRELATION HEATMAP
# ==================================================
elif page == "Correlation Heatmap":

    st.subheader("🔗 Correlation Heatmap")

    features = [
        "Price",
        "CBD_Distance",
        "Distance",
        "Rooms",
        "Landsize",
        "PricePerLand",
        "ParkingRatio"
    ]

    corr = df[features].corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==================================================
# PAGE 5: SUMMARY
# ==================================================
else:
    st.subheader("📊 Data Visualization Playground")

    st.write(
        "Use this playground to explore relationships in the cleaned dataset by creating simple univariate or bivariate scatter plots."
    )

    # Get numeric columns only (scatter plots need numbers)
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    if len(numeric_cols) < 1:
        st.warning("No numeric columns available for plotting.")
    else:
        # Plot type selector
        plot_type = st.radio(
            "Select plot type",
            ["Univariate Scatter", "Bivariate Scatter"],
            horizontal=True
        )

        # Univariate scatter
        if plot_type == "Univariate Scatter":
            y_col = st.selectbox(
                "Select a column",
                numeric_cols
            )

            fig = px.scatter(
                df,
                y=y_col,
                title=f"Univariate Scatter Plot: {y_col}"
            )

            st.plotly_chart(fig, use_container_width=True)

        # Bivariate scatter
        else:
            x_col = st.selectbox(
                "Select X-axis column",
                numeric_cols
            )

            y_col = st.selectbox(
                "Select Y-axis column",
                numeric_cols,
                index=1 if len(numeric_cols) > 1 else 0
            )

            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f"{y_col} vs {x_col}"
            )

            st.plotly_chart(fig, use_container_width=True)
