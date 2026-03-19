# Real-Time ASL Sign Language Detector

A real-time American Sign Language (ASL) detection system built with computer vision and deep learning. This project uses MediaPipe for hand tracking and an LSTM neural network to recognize ASL hand gestures through a webcam, displayed through a Flask web interface.

## Acknowledgements

This project was built following the tutorial by **PiAnalytix** — [Real-Time Sign Language Detection Machine Learning Project](https://www.youtube.com/@pianalytixofficial). The original source code and project concept belong to PiAnalytix. This repository is my own implementation and extension of their tutorial, with additional features including:
- Automated A-Z letter folder management
- Full alphabet support (A-Z) instead of just A-C
- Flask web frontend for browser-based detection
- Improved data collection interface with navigation controls

## Project Overview

- Collect hand gesture images via webcam for each ASL letter
- Extract hand keypoints using MediaPipe
- Train an LSTM neural network on those keypoints
- Detect ASL signs in real time through a browser interface

## Tech Stack

- Python 3.12
- OpenCV
- MediaPipe
- TensorFlow / Keras
- Flask
- NumPy
- scikit-learn

## Prerequisites

**1. Install dependencies**
```bash
py -3.12 -m pip install opencv-python numpy mediapipe tensorflow scikit-learn flask protobuf==4.25.3
```

**2. Create the image folder**
```bash
mkdir Image
```
The collect_data.py script will automatically create subfolders for each letter inside this folder.

## How To Run

Before anything else, make sure your environment is set up and all dependencies are installed. The steps below follow the exact order the pipeline needs to run.

**Step 1 — Initialize the helper functions**

function.py does not need to be run directly but make sure it is in the same folder as all other files. It powers everything else behind the scenes.

**Step 2 — Collect hand sign images**
```bash
py -3.12 collect_data.py
```
A webcam window will open. Use the controls below to navigate through each letter and capture photos of your hand signs. Capture 25-30 photos per letter for best results.

- Press `D` to go to the next letter
- Press `A` to go back to the previous letter
- Press `SPACE` to capture a photo
- Press `Q` to quit

**Step 3 — Extract keypoints from your images**
```bash
py -3.12 data.py
```
This will automatically process every photo you collected and extract the hand keypoints from them. You will see messages in the terminal telling you whether a hand was detected in each image.

**Step 4 — Train the model**
```bash
py -3.12 train_model.py
```
The longest step. The model will train for 200 epochs which can take anywhere from 10-30 minutes depending on your machine. Once finished it will save model.json and model.h5 to your project folder automatically.

**Step 5 — Run the app**

For the browser based web app:
```bash
py -3.12 "PY code/App_Flask.py"
```
Then open your browser and go to `http://127.0.0.1:5000`

For the standalone desktop window:
```bash
py -3.12 app.py
```

## Notes

- `model.h5` is excluded from this repository due to file size. however, using trainmodel.py will generate it. 
- `MP_Data/` and `Image/` are also excluded for the same reason.
- This project was developed and tested on Python 3.12 and Windows 11.

## License

This project is for personal education. Original tutorial and concept by PiAnalytix.