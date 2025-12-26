import streamlit as st
import cv2
import os
from datetime import datetime
from upload_to_s3 import uploadToS3
import base64
# import torch
# import random, string
from datetime import datetime,timedelta

import logging

# Create and configure logger
logging.basicConfig(filename="./sp-logs.log",
                    format='%(asctime)s %(message)s %(levelname)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)



def hide_streamlit_style():
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}  /* Hides the hamburger menu */
    footer {visibility: hidden;}    /* Hides the footer */
    header {visibility: hidden;}    /* Hides the top header */
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Configure the Streamlit app
st.set_page_config(page_title="Steel Pipes Info", layout="wide")
hide_streamlit_style()
# App-wide styles
st.markdown(
    """
    <style>
    .chat-container {
        background-color: #f7f7f7;
        border-radius: 10px;
        padding: 20px;
        max-height: 500px;
        overflow-y: auto;
    }
    .user-message {
        background-color: #d1e7ff;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: right;
    }
    .bot-message {
        background-color: #e9ecef;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
    }
    .input-box {
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def add_bg_from_local(image_file):
    """Set a background image for the Streamlit app using a local file."""
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    
    # Define CSS to set the background image
    bg_image_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_image_css, unsafe_allow_html=True)







def save_image(image):
    # Create a directory to store captured images if it doesn't exist
    save_dir = "captured_images"
    os.makedirs(save_dir, exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{save_dir}/captured_image_{timestamp}.png"
    
    # Save the image
    try:
        # Convert BGR to RGB (OpenCV default is BGR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Save the image
        cv2.imwrite(filename, image)
        
        return filename
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None
    
def save_uploaded_image(uploaded_file):
    # Create a directory to store uploaded images if it doesn't exist
    save_dir = "uploaded_images"
    os.makedirs(save_dir, exist_ok=True)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_extension = uploaded_file.name.split('.')[-1]
    filename = f"{save_dir}/uploaded_image_{timestamp}.{file_extension}"
    
    # Save the uploaded file
    try:
        with open(filename, "wb") as f:
            f.write(uploaded_file.getbuffer())

        uploadToS3(file_name=filename, bucket="awsbucket-isbcapstone")
        return filename
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None
    
def main():
    st.markdown("<h1 style='color:white; font-family:Arial;'>Automated Steel Pipe Counting</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:white; font-family:Arial;'>Select what would you like to do:</h3>", unsafe_allow_html=True)

    # Updating the bg image
    image_path = "bg_steelpipe.png"  # Replace with the path to your image

    add_bg_from_local(image_path)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Upload New Image"):
            st.session_state.current_form = "Upload_Image"
    
    with col2:
        if st.button("Get Product Info"):
            st.session_state.current_form = "Get_Info"
    
    # Display the selected form
    if hasattr(st.session_state, 'current_form'):
        if st.session_state.current_form == "Upload_Image":
            st.switch_page("pages/invoke_model.py")
            # uploaded_file = st.file_uploader(
            #         "Choose an image", 
            #         type=['jpg', 'jpeg', 'png', 'gif', 'bmp'],
            #         help="Upload an image file of your choice"
            #     )
            # if uploaded_file is not None:
            #     st.image(uploaded_file, caption="Uploaded Image")
            #     saved_path = save_uploaded_image(uploaded_file)
            #     st.success(f"Image saved successfully at {saved_path}")


        elif st.session_state.current_form == "Get_Info":
            st.switch_page("pages/chatbot.py")

if __name__ == "__main__":
    main()
