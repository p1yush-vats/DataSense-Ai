import streamlit as st
import pandas as pd
import plotly.express as px
from utils import initialize_session_state

st.set_page_config(page_title="Automated EDA", page_icon="📊", layout="wide")
initialize_session_state()

st.title("📊 Automated Exploratory Data Analysis")

if "active_dataset_name" in st.session_state and st.session_state.active_dataset_name:
    df = st.session_state.datasets[st.session_state.active_dataset_name]["df"]
    st.header(f"Analysis of `{st.session_state.active_dataset_name}`")

    tab1, tab2, tab3 = st.tabs(["📌 Overview", "Single Column Analysis", "Relationship Analysis"])

    # --- TAB 1: OVERVIEW (No changes here) ---
    with tab1:
        # ... (Code for this tab remains the same)
        st.subheader("Key Dataset Metrics")
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(label="Total Rows", value=f"{df.shape[0]:,}")
        kpi2.metric(label="Total Columns", value=f"{df.shape[1]:,}")
        kpi3.metric(label="Duplicate Rows", value=f"{df.duplicated().sum():,}")
        kpi4.metric(label="Missing Values", value=f"{df.isnull().sum().sum():,}")
        st.subheader("Data Preview")
        st.dataframe(df.head())
        st.subheader("Descriptive Statistics")
        st.dataframe(df.describe())
        st.subheader("Correlation Heatmap")
        numeric_df = df.select_dtypes(include=['number'])
        if len(numeric_df.columns) > 1:
            fig = px.imshow(numeric_df.corr(numeric_only=True), text_auto=True, aspect="auto", title="Correlation Matrix of Numeric Columns")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough numeric columns to generate a correlation heatmap.")


    # --- TAB 2: SINGLE COLUMN ANALYSIS (Updated with Pie Chart) ---
    with tab2:
        st.subheader("Univariate (Single Column) Analysis")
        selected_col = st.selectbox("Select a column to analyze:", options=["-"] + df.columns.tolist())

        if selected_col != "-":
            col_type = df[selected_col].dtype
            st.markdown(f"**Analyzing Column:** `{selected_col}` (`{col_type}`)")

            if pd.api.types.is_numeric_dtype(col_type):
                c1, c2 = st.columns(2)
                with c1:
                    fig_hist = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}", nbins=30)
                    st.plotly_chart(fig_hist, use_container_width=True)
                with c2:
                    fig_box = px.box(df, y=selected_col, title=f"Box Plot of {selected_col}")
                    st.plotly_chart(fig_box, use_container_width=True)
            
            # --- NEW: Added Pie Chart option for categorical data ---
            elif pd.api.types.is_object_dtype(col_type) or pd.api.types.is_categorical_dtype(col_type):
                chart_type = st.radio("Select Chart Type:", ["Bar Chart", "Pie Chart"])
                
                top_20 = df[selected_col].value_counts().head(20)
                if chart_type == "Bar Chart":
                    fig = px.bar(top_20, x=top_20.index, y=top_20.values, labels={'x': selected_col, 'y': 'Count'}, title=f"Top 20 Value Counts for {selected_col}")
                elif chart_type == "Pie Chart":
                    fig = px.pie(top_20, names=top_20.index, values=top_20.values, title=f"Proportions for {selected_col}")
                st.plotly_chart(fig, use_container_width=True)

            elif pd.api.types.is_datetime64_any_dtype(col_type):
                st.write("Time Series Analysis:")
                counts_over_time = df[selected_col].dt.to_period('M').value_counts().sort_index()
                counts_over_time.index = counts_over_time.index.to_timestamp()
                fig_ts = px.line(counts_over_time, x=counts_over_time.index, y=counts_over_time.values, labels={'x': 'Date', 'y': 'Count'}, title=f"Counts over Time for {selected_col}")
                st.plotly_chart(fig_ts, use_container_width=True)

    # --- TAB 3: RELATIONSHIP ANALYSIS (Updated with Categorical vs. Categorical) ---
    with tab3:
        st.subheader("Bivariate (Relationship) Analysis")
        st.write("Explore the relationship between any two columns.")

        col_x = st.selectbox("Select X-axis column:", options=df.columns.tolist(), index=0, key="col_x")
        col_y = st.selectbox("Select Y-axis column:", options=df.columns.tolist(), index=1, key="col_y")
        
        if col_x and col_y:
            type_x = df[col_x].dtype
            type_y = df[col_y].dtype
            chart_options = []
            
            if pd.api.types.is_numeric_dtype(type_x) and pd.api.types.is_numeric_dtype(type_y):
                chart_options = ["Scatter Plot", "Line Chart"]
            elif (pd.api.types.is_object_dtype(type_x) or pd.api.types.is_categorical_dtype(type_x)) and pd.api.types.is_numeric_dtype(type_y):
                chart_options = ["Bar Chart", "Box Plot", "Violin Plot"]
            elif pd.api.types.is_numeric_dtype(type_x) and (pd.api.types.is_object_dtype(type_y) or pd.api.types.is_categorical_dtype(type_y)):
                chart_options = ["Bar Chart", "Box Plot", "Violin Plot"]
                col_x, col_y = col_y, col_x
            # --- NEW: Added logic for two categorical columns ---
            elif (pd.api.types.is_object_dtype(type_x) or pd.api.types.is_categorical_dtype(type_x)) and \
                 (pd.api.types.is_object_dtype(type_y) or pd.api.types.is_categorical_dtype(type_y)):
                chart_options = ["Grouped Bar Chart"]

            if chart_options:
                selected_chart = st.selectbox("Select Chart Type:", options=chart_options)
                st.markdown("---")
                st.subheader(f"Displaying: {selected_chart}")

                if selected_chart == "Grouped Bar Chart":
                    grouped_data = df.groupby([col_x, col_y]).size().reset_index(name='count')
                    fig = px.bar(grouped_data, x=col_x, y='count', color=col_y, barmode='group', title=f"{col_x} vs. {col_y}")
                    st.plotly_chart(fig, use_container_width=True)
                # ... (rest of the chart rendering logic remains the same)
                elif selected_chart == "Scatter Plot":
                    color_option = st.selectbox("Color by (optional):", options=[None] + df.columns.tolist())
                    fig = px.scatter(df, x=col_x, y=col_y, color=color_option, title=f"{col_x} vs. {col_y}")
                    st.plotly_chart(fig, use_container_width=True)
                elif selected_chart == "Line Chart":
                    fig = px.line(df.sort_values(by=col_x), x=col_x, y=col_y, title=f"{col_x} vs. {col_y}")
                    st.plotly_chart(fig, use_container_width=True)
                elif selected_chart == "Bar Chart":
                    bar_data = df.groupby(col_x)[col_y].mean().reset_index()
                    fig = px.bar(bar_data, x=col_x, y=col_y, title=f"Average {col_y} by {col_x}")
                    st.plotly_chart(fig, use_container_width=True)
                elif selected_chart == "Box Plot":
                    fig = px.box(df, x=col_x, y=col_y, title=f"Distribution of {col_y} by {col_x}")
                    st.plotly_chart(fig, use_container_width=True)
                elif selected_chart == "Violin Plot":
                    fig = px.violin(df, x=col_x, y=col_y, title=f"Distribution of {col_y} by {col_x}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Automated plotting for this combination of column types is not yet supported.")
else:
    st.warning("Navigate to the `Chat` page and upload a dataset to begin analysis.")