from flask import Flask, render_template, Response, jsonify
import cv2
import time
from fer import FER
import os
from datetime import datetime
import threading
from PIL import Image
import numpy as np
from housekeeping import cleanup_old_captures

app = Flask(__name__)

# Global variables to store emotion data
emotion_data = []
recording = False
report_ready = False

def gen_frames():
    global recording, emotion_data
    cap = cv2.VideoCapture(0)
    detector = FER()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if recording:
            # Detect emotions
            result = detector.detect_emotions(frame)
            if result:
                emotions = result[0]['emotions']
                dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
                
                # Draw emotion text on frame
                cv2.putText(frame, dominant_emotion, (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Save emotion data if recording
                timestamp = datetime.now().strftime("%H:%M:%S")
                img_name = f"static/captures/{timestamp}_{dominant_emotion}.jpg"
                cv2.imwrite(img_name, frame)
                
                emotion_data.append({
                    'timestamp': timestamp,
                    'emotion': dominant_emotion,
                    'image_path': img_name
                })
        
        # Convert frame to jpg for streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotions')
def get_emotions():
    return jsonify({
        'recording': recording,
        'emotions': emotion_data
    })

def detect_emotions():
    global recording, emotion_data, report_ready
    
    start_time = time.time()
    
    # Create directory for saving images if it doesn't exist
    if not os.path.exists('static/captures'):
        os.makedirs('static/captures')
    
    # Wait for 15 seconds
    while recording and (time.time() - start_time) < 15:
        time.sleep(0.1)
    
    recording = False
    report_ready = True
    generate_report()

def generate_report():
    if not emotion_data:
        return
        
    with open('report.md', 'w') as f:
        f.write('# Emotion Analysis Report\n\n')
        f.write(f'Report generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        
        for entry in emotion_data:
            f.write(f'## Timestamp: {entry["timestamp"]}\n')
            f.write(f'Detected Emotion: **{entry["emotion"]}**\n\n')
            f.write(f'![Captured Frame]({entry["image_path"]})\n\n')
            f.write('---\n\n')

@app.route('/')
def index():
    return render_template('index.html', report_ready=report_ready, emotion_data=emotion_data)

@app.route('/start_recording')
def start_recording():
    global recording, emotion_data, report_ready
    
    # Run cleanup before starting new recording
    cleanup_old_captures()
    
    # Reset variables
    recording = True
    emotion_data = []
    report_ready = False
    
    # Start emotion detection in a separate thread
    thread = threading.Thread(target=detect_emotions)
    thread.start()
    
    return 'Recording started'

@app.route('/stop_recording')
def stop_recording():
    global recording, report_ready
    recording = False
    report_ready = True
    generate_report()
    return 'Recording stopped'

if __name__ == '__main__':
    app.run(debug=True) 