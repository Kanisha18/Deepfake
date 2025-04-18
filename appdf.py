# -*- coding: utf-8 -*-
"""appDF.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17FWP-wORr3br64A0nept04-_8QS7rJVp
"""

import streamlit as st
import tensorflow as tf
import numpy as np
import cv2
import tempfile
import os

# Load the model once
@st.cache_resource
def load_model():
    return tf.keras.models.load_model('Hybrid_deepfake.h5')

model = load_model()

# Preprocess the video
def preprocess_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    while count < 30:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (128, 128))  # Adjust to match your model input
        frame = frame / 255.0
        frames.append(frame)
        count += 1
    cap.release()
    return np.expand_dims(np.array(frames), axis=0)

# Streamlit UI
st.set_page_config(page_title="Deepfake Detector", layout="centered")
st.title("🔍 Deepfake Video Detector")

video_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if video_file is not None:
    # Save uploaded file temporarily
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    video_path = tfile.name

    st.video(video_file)

    if st.button("Analyze Video"):
        with st.spinner("Processing video..."):
            video_data = preprocess_video(video_path)
            prediction = model.predict(video_data)[0][0]
            result = "🟥 Fake Video" if prediction >= 0.5 else "🟩 Real Video"
            st.success(f"**Prediction:** {result}")
            st.write(f"**Confidence:** {prediction:.2f}")