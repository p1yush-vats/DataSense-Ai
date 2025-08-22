import streamlit as st
import pandas as pd
from transformers import TapasTokenizer, TapasForQuestionAnswering, pipeline
import google.generativeai as genai

# ... (load_tapas_model and initialize_session_state functions remain the same) ...
@st.cache_resource
def load_tapas_model():
    """Loads and caches the TAPAS model pipeline."""
    model_path = "./models"
    try:
        tokenizer = TapasTokenizer.from_pretrained(model_path)
        model = TapasForQuestionAnswering.from_pretrained(model_path)
        return pipeline("table-question-answering", model=model, tokenizer=tokenizer)
    except Exception as e:
        st.error(f"Error loading TAPAS model: {e}")
        return None

def initialize_session_state():
    """Initializes all necessary session state variables."""
    if "datasets" not in st.session_state:
        st.session_state.datasets = {}
    if "active_dataset_name" not in st.session_state:
        st.session_state.active_dataset_name = None


def generate_pandas_code(dataframe, query):
    """Generates and executes pandas code using a generative AI model."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # --- FINAL, MOST ROBUST PROMPT ---
        full_prompt = f"""
        You are an expert Python data analyst. Your task is to generate a single line of Python code to answer a user's question based on a pandas dataframe named 'df'.

        User Request: "{query}"
        
        The dataframe 'df' has the following columns: {list(dataframe.columns)}
        
        INSTRUCTIONS:
        - Provide only the Python code required to produce the answer.
        - NEVER use the `print()` function.
        - If the result is a table (DataFrame or Series), return the DataFrame/Series object directly. DO NOT convert it to a string.
        - **For aggregations (like 'average', 'sum', 'mean'), use the appropriate pandas method. For example, to find the average performance rating for employees with a salary over 80000, the correct code is `df[df['Salary'] > 80000]['PerformanceRating'].mean()`**.
        - If the answer is a single value (like a name or a number), the code should extract and return just that single value. For example: `df[df['Name'] == 'John Doe']['Country'].iloc[0]`
        """
        
        response = model.generate_content(full_prompt)
        generated_code = response.text.strip().replace("`", "").replace("python", "")
        
        scope = {"df": dataframe, "pd": pd}
        exec(f"result = {generated_code}", scope)
        result = scope.get('result', "Code did not produce a 'result' variable.")
        
        return generated_code, result

    except Exception as e:
        return f"An error occurred: {e}", None
# --- NEW FUNCTION TO MAKE RESPONSES CONVERSATIONAL ---
def generate_natural_language_response(query, result):
    """Generates a conversational response using the data result."""
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        prompt = f"""
        You are a helpful and friendly data analyst assistant.
        A user asked the following question: "{query}"
        
        The precise, data-driven answer is: "{result}"
        
        Your task is to formulate a friendly, complete sentence that presents this answer to the user.
        Be conversational but professional. Don't just repeat the answer; frame it nicely.
        For example, if the answer is "Daniel", you could say "The oldest employee in that region is Daniel." 
        Or if the answer is "85000", you could say "Certainly! The average salary for that department is $85,000."
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        # Fallback in case of API error, returns a simple formatted string
        return f"The answer is **{result}**."