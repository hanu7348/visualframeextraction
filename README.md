# Advanced Video Summarization

This repository contains a Streamlit application for advanced video summarization. The application allows users to upload videos, extract key frames, generate captions for each frame using pre-trained models, and summarize the captions into a coherent text summary. The application also includes user authentication and performance metrics visualization.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Expected Outcomes](#expected-outcomes)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**: Register and log in to access the video summarization functionality.
- **Video Upload**: Upload video files in formats like MP4, AVI, and MOV.
- **Frame Extraction**: Extract key frames from the uploaded video.
- **Image Captioning**: Generate captions for each extracted frame using pre-trained models.
- **Text Summarization**: Summarize the captions into a coherent text summary.
- **Performance Metrics**: Evaluate and visualize the performance of the captioning and summarization processes.
- **Responsive UI**: An intuitive and user-friendly interface developed with Streamlit.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/advanced-video-summarization.git
cd advanced-video-summarization

2. **Create a virtual environment and activate it:**
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

pip install -r requirements.txt

Run the Streamlit application:
streamlit run app.py

