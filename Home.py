import streamlit as st
from PIL import Image  
from utils import initialize_session_state

st.set_page_config(page_title="DataSense AI | Home", page_icon="🏠", layout="centered")
initialize_session_state()

st.title("Welcome to DataSense AI 🧠")
st.markdown("---")

st.markdown(
    """
    **Transform raw data into actionable insights with the power of conversational AI.**
    
    This professional-grade tool redefines data interaction. This suite includes:

    ### ✨ Key Features
    - **Multi-Dataset Management**: Upload and seamlessly switch between multiple datasets.
    - **Unified Smart Chat**: Ask both simple and complex questions in a single chat interface. The AI automatically chooses the best way to answer.
    - **Automated EDA**: Instantly generate a comprehensive Exploratory Data Analysis report.

    ### 🚀 Get Started
    1.  **Navigate to the `Chat` page** to upload your first dataset.
    2.  **Select your dataset** from the Data Manager.
    3.  **Start your conversation** or switch to the `Automated EDA` page for a deep dive.
    """
)
st.markdown("---")


st.video("https://www.youtube.com/watch?v=-oCoruI5sM8")

st.sidebar.success("Select a page above to begin.")