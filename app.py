import streamlit as st
import cv2
import numpy as np
from transformers import pipeline
from PIL import Image
import tempfile
import os
import time
from rouge import Rouge
import matplotlib.pyplot as plt
import sqlite3

# Set the page configuration for the Streamlit app
st.set_page_config(page_title="Advanced Video Summarization", layout="wide")

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            video_path TEXT,
            upload_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Cache the summarizer model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="google/pegasus-xsum")

# Cache the image captioner model
@st.cache_resource
def load_image_captioner(model_name):
    return pipeline("image-to-text", model=model_name)

# Load the summarizer
summarizer = load_summarizer()

# Function to extract frames from the video
def extract_frames(video_path, num_frames=5):
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    
    for i in range(num_frames):
        frame_idx = i * (total_frames // num_frames)
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = video.read()
        if ret:
            frames.append(frame)
    
    video.release()
    return frames

# Function to generate captions for each frame
def frames_to_captions(frames, image_captioner):
    captions = []
    times = []
    for i, frame in enumerate(frames):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        caption, elapsed_time = measure_time(lambda: image_captioner(pil_image)[0]['generated_text'])
        captions.append((rgb_frame, caption, elapsed_time))
        times.append(elapsed_time)
    
    return captions, times

# Function to summarize text using the loaded summarizer
def summarize_text(text):
    summary, elapsed_time = measure_time(lambda: summarizer(text, max_length=150, min_length=50, do_sample=False))
    return summary[0]['summary_text'], elapsed_time

# Helper function to measure the time taken by another function
def measure_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return result, elapsed_time

# Function to evaluate the summary using ROUGE scores
def evaluate_summary(reference_text, generated_text):
    rouge = Rouge()
    scores = rouge.get_scores(generated_text, reference_text)
    return scores

# Function to plot the performance metrics
def plot_metrics(times, title):
    plt.figure(figsize=(10, 5))
    plt.plot(times, marker='o')
    plt.title(title)
    plt.xlabel('Frame')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    st.pyplot(plt)

# Database functions
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        st.sidebar.success("User registered successfully! You can now log in.")
    except sqlite3.IntegrityError:
        st.sidebar.error("Username already exists. Please choose a different username.")
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    return user

def save_video_upload(user_id, video_path):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO uploads (user_id, video_path) VALUES (?, ?)', (user_id, video_path))
    conn.commit()
    conn.close()

# Streamlit app UI

# Set the background style for the Streamlit app
st.markdown(
    """
    <style>
    .stApp {
        background: url("https://techcommunity.microsoft.com/t5/image/serverpage/image-id/469874iFE0D4F020442C5F9/image-size/large?v=v2&px=999");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align: center;'>Advanced Visual Frame Extraction and Summarization</h1>", unsafe_allow_html=True)

# Sidebar for user authentication
st.sidebar.title("User Authentication")
auth_option = st.sidebar.radio("Select an option", ["Login", "Register"])

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None

if auth_option == "Register" and not st.session_state.logged_in:
    with st.sidebar.form(key="register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Register")
        if submit_button:
            register_user(username, password)

if auth_option == "Login" and not st.session_state.logged_in:
    with st.sidebar.form(key="login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            user = authenticate_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.sidebar.success("Login successful!")
            else:
                st.sidebar.error("Invalid credentials. Please try again.")

if st.session_state.logged_in:
    # File uploader for the user to upload a video file
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
    # Slider for selecting the number of frames to extract
    num_frames = st.slider("Select number of frames to extract", 1, 20, 5)

    # Dropdown for selecting the image captioning model with descriptions
    image_captioning_models = {
        "BLIP": "BLIP: Bootstrapping Language-Image Pre-training",
        
    }
    selected_model_key = st.selectbox("Select Image Captioning Model", list(image_captioning_models.keys()))
    selected_model = {
        "BLIP": "Salesforce/blip-image-captioning-base",
        
    }.get(selected_model_key, None)

    if selected_model is None:
        st.error("Selected model is not available.")
    else:
        if uploaded_file is not None:
            # Create a temporary file to store the uploaded video
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            tfile.close()
            
            # Display the uploaded video
            video_file = open(tfile.name, 'rb')
            video_bytes = video_file.read()
            st.video(video_bytes)
            video_file.close()
            
            # Button to start the summarization process
            if st.button('Summarize Video'):
                with st.spinner('Processing video...'):
                    # Extract frames from the video
                    frames, frame_time = measure_time(lambda: extract_frames(tfile.name, num_frames))
                    if not frames:
                        st.error("No frames extracted. Please check the video file.")
                    else:
                        st.write(f"Frames extracted successfully in {frame_time:.2f} seconds.")
                    
                    # Load the selected image captioner model
                    image_captioner = load_image_captioner(selected_model)
                    # Generate captions for each frame
                    captions, caption_times = frames_to_captions(frames, image_captioner)
                    all_captions_text = " ".join([caption for _, caption, _ in captions])
                    
                    # Display each frame with its caption
                    for i, (frame, caption, _) in enumerate(captions):
                        st.image(frame, caption=f"Frame {i+1}: {caption}", use_column_width=True)
                    
                    # Generate the summary from the captions
                    summary_text, summary_time = summarize_text(all_captions_text)
                
                # Display the summary
                st.subheader('Video Summary')
                st.write(summary_text)
                
                # Evaluate the summary
                reference_text = "The reference summary text goes here."  # Replace with actual reference text
                scores = evaluate_summary(reference_text, summary_text)
                st.subheader('Summary Evaluation')
                st.write(f"ROUGE Scores: {scores}")
                st.write(f"Summary generated in {summary_time:.2f} seconds.")
                
                # Plot the performance metrics
                st.subheader('Performance Metrics')
                plot_metrics(caption_times, 'Caption Generation Time per Frame')

                # Save video upload information
                save_video_upload(st.session_state.user_id, tfile.name)
                    
                # Clean up the temporary file
                try:
                    os.unlink(tfile.name)
                except PermissionError:
                    st.warning("Unable to delete temporary file. It will be deleted when you close the application.")
else:
    st.sidebar.info("Please log in to access the video summarization functionality.")
