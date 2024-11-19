import streamlit as st
import pandas as pd
from copulas.multivariate import GaussianMultivariate
import io

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

if uploaded_file:
    # Read the uploaded CSV file
    real_data = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Sample")
    st.write(real_data.head())

    if generate_button:
        st.write("### Generating Synthetic Data...")

        # Initialize the Gaussian copula model
        model = GaussianMultivariate()

        # Fit the model on the uploaded data
        model.fit(real_data)

        # Generate synthetic data
        synthetic_data = model.sample(num_samples)

        st.write("### Synthetic Data Sample")
        st.write(synthetic_data.head())

        # Convert synthetic data to CSV for download
        csv_buffer = io.BytesIO()
        synthetic_data.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        # Create a download button
        st.download_button(
            label="Download Synthetic Data",
            data=csv_buffer,
            file_name="synthetic_data.csv",
            mime="text/csv"
        )