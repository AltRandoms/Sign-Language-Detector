from flask import Flask, render_template, Response
from function import *
from keras.models import model_from_json
import numpy as np
import cv2
import os

app = Flask(__name__)

# Get the exact folder where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model using absolute paths
json_file = open(os.path.join(BASE_DIR, "model.json"), "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights(os.path.join(BASE_DIR, "model.h5"))

sequence = []
sentence = []
accuracy = []
predictions = []
threshold = 0.8

def generate_frames():
    global sequence, sentence, accuracy, predictions
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            cropframe = frame[40:400, 0:300]
            frame = cv2.rectangle(frame, (0, 40), (300, 400), (255, 255, 255), 2)
            image, results = mediapipe_detection(cropframe, hands)
            draw_styled_landmarks(image, results)

            keypoints = extract_keypoints(results)
            sequence.append(keypoints)
            sequence = sequence[-30:]

            label = ""
            conf = ""

            try:
                if len(sequence) == 30:
                    res = model.predict(np.expand_dims(sequence, axis=0), verbose=0)[0]
                    predictions.append(np.argmax(res))

                    if np.unique(predictions[-10:])[0] == np.argmax(res):
                        if res[np.argmax(res)] > threshold:
                            label = actions[np.argmax(res)]
                            conf = f"{res[np.argmax(res)] * 100:.1f}%"
                            if len(sentence) == 0 or sentence[-1] != label:
                                sentence.append(label)
                                accuracy.append(conf)

                    if len(sentence) > 1:
                        sentence = sentence[-1:]
                        accuracy = accuracy[-1:]

            except Exception:
                pass

            # Draw output bar on frame
            cv2.rectangle(frame, (0, 0), (300, 38), (245, 117, 16), -1)
            display = f"{label}  {conf}" if label else "Waiting..."
            cv2.putText(frame, display, (5, 27),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # Encode frame for streaming
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=False)