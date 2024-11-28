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

            if "creditscore" in column.lower():
                row.append(random.randint(300, 850))
            elif "geography" in column.lower():
                row.append(fake.country())
            elif "gender" in column.lower():
                row.append(random.choice(["Male", "Female"]))
            elif "age" in column.lower():
                row.append(random.randint(18, 100))
            elif "tenure" in column.lower():
                row.append(random.randint(0, 40))
            elif "estimatedsalary" in column.lower():
                row.append(round(random.uniform(20000, 150000), 2))
            elif "city" in column.lower():
                row.append(fake.city())
            elif "state" in column.lower() or "region" in column.lower():
                row.append(fake.state())
            elif "country" in column.lower():
                row.append(fake.country())
            elif "name" in column.lower():
                row.append(fake.name())
            elif "email" in column.lower():
                row.append(fake.email())
            elif "address" in column.lower():
                row.append(fake.address())
            elif "phone" in column.lower():
                row.append(fake.phone_number())
            elif "company" in column.lower():
                row.append(fake.company())
            elif "job" in column.lower():
                row.append(fake.job())
            elif "credit card" in column.lower():
                row.append(fake.credit_card_number())
            elif "url" in column.lower():
                row.append(fake.url())
            elif "ip" in column.lower():
                row.append(fake.ipv4())
            elif "date" in column.lower():
                row.append(fake.date_between(start_date='-30y', end_date='today'))
            elif "postcode" in column.lower() or "zip" in column.lower():
                row.append(fake.postcode())
            elif "$" in str(sample_value):
                row.append(f"${round(random.uniform(0, 100000), 2)}")
            else:
                row.append(fake.word())
        
        synthetic_data.append(row)

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