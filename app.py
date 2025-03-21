import streamlit as st 
from PIL import Image 
import pandas as pd
from faker import Faker
import io
import random
import re
import pathlib




# calling style css
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("assets/style.css")
load_css(css_path)



# --- CSS to style the sidebar and apply custom font with weights ---
st.markdown(
    """
    <style>
        /* Import Poppins font */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

        /* Apply Poppins to the whole app */
        body, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 {
            font-family: 'Poppins', sans-serif;
        }

        [data-testid="stSidebar"] {
            background-color: #280071;
        }

        [data-testid="stSidebarHeader"] img {
            display: block;
            margin: 0 auto;
            width: 80%;
        }

        button[data-testid="stBaseButton-secondary"] {
            border: 1px solid #280071;  
            color: #280071;
            transition: 0.3s ease;
        }

        button[data-testid="stBaseButton-secondary"]:hover {
            border-color: #280071;
            color: #280071;
        }

        button[data-testid="stBaseButton-secondary"]:active {
            color: rgb(255, 255, 255);
            border-color: #280071;
            background-color: #280071;
        }

        button[data-testid="stBaseButton-secondary"]:focus-visible {
            box-shadow: #2800712b 0px 0px 0px 0.2rem;
        }

        button[data-testid="stBaseButton-secondary"]:focus:not(:active) {
            color: #280071;
            border-color: #280071;
                background: white;
        }

        div[data-testid="stFileUploaderFileName"] {
            color: #ffffff; 
            font-weight: bold; 
            font-size: 16px;
        }

        div[data-testid="stFileUploaderFileName"]:hover {
            color: #ffffff;
        }

        small[data-testid="st-emotion-cache-1rpn56r"]:hover {
            color: #ffffff;
        }

        small.ejh2rmr0:nth-of-type(1) {
            color: #75787B; 
            font-weight: regular;
            font-size: 14px;
        }

        .st-emotion-cache-1oq9q35 {
            font-family: 'Poppins', sans-serif;
            font-size: 0.875rem;
            color: rgb(255, 255, 255);
        }

        .st-emotion-cache-8ccstr {
            color:white !important;
        }

        .st-emotion-cache-m2hdlh:hover:enabled,
        .st-emotion-cache-m2hdlh:focus:enabled {
            color: rgb(255, 255, 255);
            background-color: #EACBBB;
            transition: none;
            outline: none;
        }

        .st-emotion-cache-12fmjuu {
            background: rgb(248 248 248);
        }

        .st-emotion-cache-1104ytp h3 {
    font-size: 1.75rem;
    padding: 0.5rem 0px 1rem;
    font-family: 'Poppins';
}


.st-emotion-cache-1hyd1ho{
   font-family: 'Poppins';
}

.st-emotion-cache-179n174 {
    display: inline;
    transition: left 300ms;
    color: rgb(198 207 255);
    line-height: 0;
}
.st-emotion-cache-m2is37 {
    color: rgb(198 207 255);
 

}

button[data-testid="stBaseButton-secondary"] {
    border: 1px solid #280071;
    color: #280071;
    transition: 0.3s ease;
    background: white;
}


    </style>
    """,
    unsafe_allow_html=True,
)


# Initialize Faker
fake = Faker()







svg_img_path = "assets/data_icon.svg"

with open(svg_img_path, "r") as svg_file:
    svg_content = svg_file.read()
st.markdown(
    f'<div style="text-align: center;">{svg_content}</div>',
    unsafe_allow_html=True
)


# Title for the app
st.markdown(
    "<h2 style=color:#282C2F;text-align:center;font-family:Poppins;font-size:24px;>Synthetic Data Generator</h2>",
  unsafe_allow_html=True
)

st.markdown(
    "<p style=font-size:14px;text-align:center;margin-bottom:15px;margin-top:-10px;line-height:22px;color:##53565A;font-family:Poppins;>No data uploaded yet. Start by uploading a CSV file to generate synthetic data Once uploaded, choose the number of samples and click Generate Synthetic Data to proceed</p>",
  unsafe_allow_html=True
)


# Load and display an SVG logo inside the sidebar header
svg_logo_path = "assets/logo/tietoevry_logo.svg"

with st.sidebar:
    # Read and display SVG directly in sidebar header
    with open(svg_logo_path, "r") as svg_file:
        svg_logo = svg_file.read()






    st.markdown(
        f'<div  data-testid="stSidebarHeader"  style=width:60%;>{svg_logo}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
    "<h3 style=color:white;text-align:left;margin-top:30px;margin-bottom:15px;>Upload sample data and generate synthetic test data</h3>",
  unsafe_allow_html=True
)








    uploaded_file = st.file_uploader("Upload your CSV file", type="csv", key="white")

    st.markdown("<div  style=margin-top:15px;margin-bottom:15px;> </div>", unsafe_allow_html=True)

    # Input for number of synthetic samples
    num_samples = st.number_input(
        "Number of synthetic samples to generate", min_value=1, value=100
    )
    st.markdown("<div  style=margin-top:15px;margin-bottom:15px;> </div>", unsafe_allow_html=True)


    # Button to trigger synthetic data generation
    generate_button = st.button("Generate Synthetic Data", key="green")


# Function to generate synthetic data
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
