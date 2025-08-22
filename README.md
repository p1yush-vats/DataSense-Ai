# DataSense AI 🧠

**Bridging the Gap Between Complex Data and Conversational Insight**

---

## Overview

In an era where data is paramount, the ability to extract meaningful insights remains a significant bottleneck for many. DataSense AI emerges as a paradigm-shifting solution, designed to democratize data analysis. It empowers users, regardless of their technical expertise, to engage in a direct, intuitive dialogue with their data, transforming complex queries into clear, actionable intelligence.

---

## ✨ Core Capabilities

- **Dynamic Multi-Dataset Workspace:**  
  Seamlessly upload, preview, and switch between multiple datasets within a persistent session. Each dataset maintains its own context, including conversational history.

- **Intelligent Conversational Engine:**  
  Leveraging Google's Gemini, the unified chat interface translates natural language queries into executable Python (pandas) code. It handles everything from simple lookups to complex, multi-step analytical questions with remarkable precision.

- **Comprehensive Automated EDA Suite:**  
  Automatically generate a rich, interactive dashboard featuring:
  - Key performance indicators (KPIs) of the dataset's health.
  - In-depth univariate analysis with adaptive visualizations (histograms, box plots, pie charts).
  - Bivariate analysis to uncover relationships between columns using appropriate charts (scatter plots, grouped bar charts, etc.).

- **User-Centric Design:**  
  A polished interface with selectable custom themes, collapsible code snippets, and a universally compatible date-column converter ensures a fluid and intuitive user experience.

---

## 🚀 Workflow

1. **Initiation:**  
   Users greeted by a clean landing page, navigating to the Chat interface to begin.

2. **Ingestion:**  
   Load the pre-packaged demo dataset with a single click or upload your own CSV files. The intelligent date-converter helps prepare datasets for time-based analysis.

3. **Interaction & Analysis:**  
   Engage in a dialogue with the AI to query data. Switch to the Automated EDA page anytime for a comprehensive visual and statistical summary of the active dataset.

---

## 🛠️ Architectural Blueprint

**Frontend Framework:**  
- Streamlit — For an interactive, stateful, and rapidly developed web interface.

**Data Manipulation:**  
- Pandas — Core for backend data wrangling, aggregation, and analysis.

**Plotting Engine:**  
- Plotly — Powers all dynamic, interactive, and publication-quality visualizations.

**AI Core:**  
- **Google Gemini:** Main reasoning engine, interpreting user intent and generating precise Python code.  
- **Hugging Face Transformers (TAPAS):** For rudimentary table Q&A, demonstrating a hybrid AI architecture.

---

## 🏁 Local Deployment Guide

### Prerequisites

- Python 3.8+
- Git and Git LFS installed
- A Google Gemini API Key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/p1yush-vats/DataSense-Ai.git
```

2. Navigate to the project directory:

```bash
cd DataSense-Ai
```

3. Install the required libraries:

```bash
pip install -r requirements.txt
```

### Configuration

1. Create a secrets file:

In the `.streamlit` folder, create a new file named `secrets.toml`.

2. Add your API key:

```toml
GOOGLE_API_KEY = "YOUR_API_KEY_HERE"
```

### Running the App

Start the application:

```bash
streamlit run Home.py
```

Your default web browser will automatically open with the running application.

---

## Contact & Support

For questions, issues, or contributions, please open an issue or pull request on the [GitHub repository](https://github.com/p1yush-vats/DataSense-Ai).

---

*Thank you for exploring DataSense AI — Making Data Analysis Conversational and Accessible!*