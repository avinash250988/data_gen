import streamlit as st
import pandas as pd
from faker import Faker
import io
import random
import re

# Initialize Faker
fake = Faker()

# Title for the app
st.title("Synthetic Data Generator")

# File upload section
st.sidebar.header("Upload Data and Generate Synthetic Data")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type="csv")

# Input for the number of synthetic samples
num_samples = st.sidebar.number_input(
    "Number of synthetic samples to generate", min_value=1, value=100
)

# Button to trigger synthetic data generation
generate_button = st.sidebar.button("Generate Synthetic Data")

def generate_synthetic_data(real_data, num_samples):
    synthetic_data = []

    for _ in range(num_samples):
        row = []
        for column in real_data.columns:
            sample_value = real_data[column].dropna().iloc[0] if not real_data[column].dropna().empty else ""

            if real_data[column].dtype == 'object':
                if re.search(r'\d', sample_value) and re.search(r'[a-zA-Z]', sample_value):
                    # Alphanumeric pattern
                    row.append(fake.bothify(text='??-####'))
                elif re.search(r'\$', sample_value):
                    # Dollar amount pattern
                    row.append(f"${random.uniform(1, 1000):.2f}")
                else:
                    # Generic string
                    row.append(fake.word())
            elif real_data[column].dtype in ['int64', 'float64']:
                # Generate random numbers for numeric columns
                row.append(fake.random_number(digits=5))
            else:
                # Default to random alphanumeric strings for any other types
                row.append(fake.bothify(text='??-####'))
        
        synthetic_data.append(row)

    # Create DataFrame with the same columns as the original data
    synthetic_df = pd.DataFrame(synthetic_data, columns=real_data.columns)

    return synthetic_df

if uploaded_file:
    # Read the uploaded CSV file
    real_data = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Sample")
    st.write(real_data.head())

    if generate_button:
        st.write("### Generating Synthetic Data...")

        # Generate synthetic data
        synthetic_df = generate_synthetic_data(real_data, num_samples)

        st.write("### Synthetic Data Sample")
        st.write(synthetic_df.head())

        # Convert synthetic data to CSV for download
        csv_buffer = io.BytesIO()
        synthetic_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        # Create a download button
        st.download_button(
            label="Download Synthetic Data",
            data=csv_buffer,
            file_name="synthetic_data.csv",
            mime="text/csv"
        )