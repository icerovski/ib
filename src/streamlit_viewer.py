import streamlit as st

def display_sections(dataframes):
    """
    Function to display a dictionary of Pandas DataFrames in Streamlit.

    Args:
        dataframes (dict): Dictionary where keys are section names and values are Pandas DataFrames.
    """
    st.title("CSV Section Viewer")

    # Iterate through sections and display each DataFrame
    for section, df in dataframes.items():
        with st.expander(f"📊 {section}"):
            st.dataframe(df)  # Display DataFrame
