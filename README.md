# 📹 Advanced Video Summarization

This repository contains a Streamlit application for advanced video summarization. The application allows users to upload videos, extract key frames, generate captions for each frame using pre-trained models, and summarize the captions into a coherent text summary. The application also includes user authentication and performance metrics visualization.

## 📋 Table of Contents

- [✨ Features](#-features)
- [⚙️ Installation](#-installation)
- [🚀 Usage](#-usage)
- [🔧 Technologies Used](#-technologies-used)
- [🎯 Expected Outcomes](#-expected-outcomes)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)

## ✨ Features

- **🔐 User Authentication**: Register and log in to access the video summarization functionality.
- **📤 Video Upload**: Upload video files in formats like MP4, AVI, and MOV.
- **🖼️ Frame Extraction**: Extract key frames from the uploaded video.
- **📝 Image Captioning**: Generate captions for each extracted frame using pre-trained models.
- **📰 Text Summarization**: Summarize the captions into a coherent text summary.
- **📊 Performance Metrics**: Evaluate and visualize the performance of the captioning and summarization processes.
- **💻 Responsive UI**: An intuitive and user-friendly interface developed with Streamlit.

## ⚙️ Installation

To run this application locally, follow these steps:

1. **📥 Clone the repository:**

    ```bash
    git clone https://github.com/your-username/advanced-video-summarization.git
    cd advanced-video-summarization
    ```

2. **🐍 Create a virtual environment and activate it:**

    ```bash
    python3 -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **📦 Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **🚀 Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

## 🚀 Usage

1. Open your web browser and go to `http://localhost:8501`.
2. Register or log in using the sidebar.
3. Upload a video file.
4. Select the number of frames to extract and the image captioning model.
5. Click the "Summarize Video" button to start the summarization process.
6. View the extracted frames, generated captions, and the final summary.
7. Evaluate the summary and visualize performance metrics.

## 🔧 Technologies Used

### Tools

- **Streamlit**: For building the web application.
- **OpenCV**: For video frame extraction and manipulation.
- **FFmpeg**: For video processing tasks.
- **Bootstrap**: For responsive and visually appealing UI components.
- **SQLite**: For user authentication and storing video uploads.

### Technologies

- **Python 3.x**: For running the application and various libraries.
- **HTML/CSS/JavaScript**: For developing the front-end interface of the web application.
- **Hugging Face Transformers**: For utilizing pre-trained models for summarization and image captioning.
- **ROUGE**: For evaluating the quality of generated summaries.
- **Pandas**: For data manipulation and analysis.

## 🎯 Expected Outcomes

1. Efficient extraction of key frames from input videos.
2. High-quality and concise textual summaries of videos.
3. An intuitive and user-friendly web interface.
4. Accurate evaluation of summaries using ROUGE scores.
5. Optimized performance for real-time video processing and summarization.
6. Scalable solution to handle large volumes of video data.
7. Comprehensive documentation of the development process and results.

## 🤝 Contributing

Contributions are welcome! If you have any suggestions or improvements, please create a pull request or open an issue.

