import streamlit as st
import cv2
import os
from upload_to_s3 import uploadToS3
import random, string
from datetime import datetime,timedelta
import configparser
from ultralytics import YOLO
import numpy as np
# import webcam
import psycopg
from psycopg import sql
from PIL import Image
import torch
import boto3


# Custom CSS for aesthetics
custom_css = """
<style>
.aesthetic-markdown {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 1.2rem;
    line-height: 1.6;
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    color: #333;
    max-width: 700px;
    margin: auto;
    text-align: justify;
}
.aesthetic-markdown h1 {
    color: #2c3e50;
    font-size: 2rem;
}
.aesthetic-markdown h2 {
    color: #34495e;
    font-size: 1.5rem;
}
.aesthetic-markdown p {
    color: #555;
}
.aesthetic-markdown a {
    color: #3498db;
    text-decoration: none;
    font-weight: bold;
}
.aesthetic-markdown a:hover {
    text-decoration: underline;
}
</style>
"""

# Injecting custom CSS
st.markdown(custom_css, unsafe_allow_html=True)




# Function to download the latest model from S3
def download_model(bucket, key):

    obj = boto3.client("s3")


    obj.download_file(
        Filename="best.pt",
        Bucket=bucket,
        Key=key
    )

    obj.close()


# Reading the config files
config = configparser.ConfigParser()
config.read('config.ini')


host = config["POSTGRES"]["host"]
port = config["POSTGRES"]["port"]
user = config["POSTGRES"]["user"]



password = config["POSTGRES"]["password"]


s3_bucket = config["MODEL"]["bucket"]
model_s3_key = config["MODEL"]["model_key"]


s3_object_bucket = config["OBJECT_STORAGE"]["bucket"]


st.title("Steel Pipe Counting Software")
    

def count_pipes(model_path, image_path):
    """
    Detect and count pipes of different shapes using a trained YOLO model
    
    Args:
        model_path (str): Path to the trained YOLO model (.pt file)
        image_path (str): Path to the input image
    
    Returns:
        dict: Counts of pipes for each shape
    """
    # Load the trained YOLO model
    model = YOLO(model_path)
    
    # Perform inference
    results = model(image_path)
    results=model.predict(source=image_path,save=True,conf=0.1,max_det=1000)
    print("Model Invoked")
    # Initialize shape counters
    shape_counts = {
        'circular': 0,
        'rectangular': 0, 
        'square': 0,
        'hexagonal': 0
    }

    c = 0
    h = 0
    s1  = 0
    s2 = 0
    for box in results[0].boxes:
        class_id = int(box.cls)
        classname = model.names[class_id]
        if classname == 'c':
            c = c+1
        if classname == 'h':
            h = h+1
        if classname == 's1':
            s1 = s1+1
        if classname == 's2':
            s2 = s2+1
    print('Circular : ' + str(c) + ' Hex : ' + str(h) + ' Square 1 : ' + str(s1) + ' Square 2: ' + str(s2))
    shape_counts = {
        'circular': c,
        'rectangular': s1, 
        'square': s2,
        'hexagonal': h
    }
    

    
    return shape_counts


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

        uploadToS3(file_name=filename, bucket=s3_object_bucket)
        return filename
    except Exception as e:
        st.error(f"Error saving image: {e}")
        return None
    
def generate_image_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=4))


    
saved_path = None



if uploaded_file:= st.file_uploader(
            "Choose an image", 
            type=['jpg', 'jpeg', 'png', 'gif', 'bmp'],
            help="Upload an image file of your choice"
        ):
    # uploaded_file 
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image")
        saved_path = save_uploaded_image(uploaded_file)
if saved_path:
    st.success(f"Image saved successfully at {saved_path}")
    # download_model(s3_bucket,model_s3_key)
    model_path = 'best.pt'

    # retrieving the pipe counts
    pipe_counts = count_pipes(model_path, saved_path)

    no_of_square_pipes = pipe_counts["square"]
    no_of_rectangle_pipes = pipe_counts["rectangular"]
    no_of_circle_pipes = pipe_counts["circular"]
    no_of_hexagon_pipes = pipe_counts["hexagonal"]
    total_pipes = no_of_square_pipes + no_of_rectangle_pipes +no_of_circle_pipes  + no_of_hexagon_pipes
    image_id = saved_path.split("/")[-1].split(".")[0]+"-"+generate_image_id()
    updation_time = datetime.now()
    # updating the info to Database
    insert_query = """
    INSERT INTO steelpipes (image_id, no_of_square_pipes,no_of_rectangle_pipes,no_of_circle_pipes,no_of_hexagon_pipes,total_pipes ,updation_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """



    connection = psycopg.connect(host=host, user=user, password=password,  port=port)
    cursor = connection.cursor()
    connection.autocommit = True 
    cursor.execute(insert_query, (image_id, no_of_square_pipes,no_of_rectangle_pipes,no_of_circle_pipes,no_of_hexagon_pipes,total_pipes, updation_time))

    st.write("For the uploaded image, Following are the respective Pipe Counts:")
    st.markdown("<h2>Shapes:</h2>",unsafe_allow_html=True)
    for shape, count in pipe_counts.items():
        # st.write()
        st.markdown(f"{shape.capitalize()} Pipes: {count}", unsafe_allow_html=True)