import streamlit as st
import pandas as pd
import os

st.title("Hackathon Data Viewer")
st.write("This app displays the latest hackathon data from Devpost and MLH.")

# Path to the combined CSV file
csv_path = "data/combined_hackathons.csv"

if os.path.exists(csv_path):
    # Read and display the data
    df = pd.read_csv(csv_path)
    st.write("### Combined Hackathon Data")
    st.dataframe(df)
else:
    st.write("No hackathon data available. Please check back later.")
