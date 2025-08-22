import streamlit as st
import pandas as pd
from utils import initialize_session_state, generate_pandas_code

# --- FIX: st.set_page_config() is now the first Streamlit command ---
st.set_page_config(page_title="Unified Chat", page_icon="💬", layout="wide")

# Custom CSS for a visible scrollbar in the sidebar
st.markdown("""
<style>
    [data-testid="stSidebarUserContent"]::-webkit-scrollbar {
        width: 8px;
    }
    [data-testid="stSidebarUserContent"]::-webkit-scrollbar-track {
        background: #f1f1f1; 
    }
    [data-testid="stSidebarUserContent"]::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 4px;
    }
    [data-testid="stSidebarUserContent"]::-webkit-scrollbar-thumb:hover {
        background: #555; 
    }
</style>
""", unsafe_allow_html=True)

initialize_session_state()

st.title("💬 Unified AI Chat")
st.markdown("Ask any question about your data, from simple lookups to complex analysis.")

# --- Sidebar ---
with st.sidebar:
    st.header("🗂️ Data Manager")
    
    st.markdown("#### Try with a demo dataset")
    if st.button("Load Demo Data"):
        try:
            df = pd.read_csv("data/employee_data.csv", parse_dates=['HireDate'])
            dataset_name = "demo_employee_data.csv"
            st.session_state.datasets[dataset_name] = {"df": df, "messages": []}
            st.session_state.active_dataset_name = dataset_name
            st.success("Demo data loaded successfully!")
            st.rerun()
        except FileNotFoundError:
            st.error("Demo file not found. Make sure 'employee_data.csv' is in a 'data' folder.")
    
    st.markdown("---")
    st.markdown("#### Upload your own data")
    uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            dataset_name = file.name
            if dataset_name not in st.session_state.datasets:
                df = pd.read_csv(file)
                st.session_state.datasets[dataset_name] = {"df": df, "messages": []}
                st.session_state.active_dataset_name = dataset_name
        st.success("Files uploaded!")

    if st.session_state.datasets:
        dataset_names = list(st.session_state.datasets.keys())
        try:
            active_index = dataset_names.index(st.session_state.active_dataset_name)
        except (ValueError, TypeError):
            active_index = 0
        st.session_state.active_dataset_name = st.selectbox("Select active dataset:", options=dataset_names, index=active_index)
        
        st.subheader("Active Data Preview")
        preview_df = st.session_state.datasets[st.session_state.active_dataset_name]["df"]
        st.dataframe(preview_df.head(), use_container_width=True)
        
        st.subheader("🗓️ Date Column Converter")
        df_active = st.session_state.datasets[st.session_state.active_dataset_name]["df"]
        potential_date_cols = [col for col in df_active.columns if df_active[col].dtype == 'object']
        detected_date_cols = []
        for col in potential_date_cols:
            try:
                if pd.to_datetime(df_active[col].sample(n=min(10, len(df_active)), replace=True), errors='coerce').notna().sum() > 5:
                    detected_date_cols.append(col)
            except Exception:
                continue
        selected_date_cols = st.multiselect("Select columns to convert to date format:", options=df_active.columns, default=detected_date_cols)
        if st.button("Convert Selected Columns"):
            for col in selected_date_cols:
                try:
                    df_active[col] = pd.to_datetime(df_active[col], errors='coerce')
                except Exception as e:
                    st.warning(f"Could not convert '{col}': {e}")
            st.success("Date columns converted!")
            st.rerun()
    else:
        st.session_state.active_dataset_name = None

# --- Main Chat Interface (No changes below this line) ---
if st.session_state.active_dataset_name:
    # ... (The rest of the file remains the same)
    active_dataset = st.session_state.datasets[st.session_state.active_dataset_name]
    st.header(f"Conversation with `{st.session_state.active_dataset_name}`")

    for message in active_dataset["messages"]:
        with st.chat_message(message["role"]):
            content = message["content"]
            if isinstance(content, tuple) and len(content) == 2:
                code, display_obj = content
                if isinstance(display_obj, (pd.DataFrame, pd.Series)):
                    st.dataframe(display_obj)
                else:
                    st.markdown(display_obj)
                with st.expander("View Generated Code"):
                    st.code(code, language="python")
            else:
                st.markdown(content)
    
    if prompt := st.chat_input("Ask any question about your data..."):
        active_dataset["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("🧠 Thinking..."):
                response_for_history = None
                code, result = generate_pandas_code(active_dataset["df"], prompt)
                
                if result is not None:
                    if isinstance(result, (pd.DataFrame, pd.Series)):
                        st.dataframe(result)
                        response_for_history = (code, result)
                    else:

                        st.markdown(f"The answer is: **{result}**")
                        response_for_history = (code, result)
                    
                    with st.expander("View Generated Code"):
                        st.code(code, language="python")
                else:
                    st.error(code) 
                    response_for_history = code

        if response_for_history is not None:
            active_dataset["messages"].append({"role": "assistant", "content": response_for_history})
else:
    st.info("Upload a CSV file or load the demo data to begin your analysis.")