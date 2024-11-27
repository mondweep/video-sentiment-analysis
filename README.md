# Video Sentiment Analyzer

A real-time emotion detection application that captures and analyzes facial expressions using your webcam. The application records emotions for 15 seconds and generates a report with timestamped images showing detected emotions.

## Architecture

### Components
1. **Web Interface (Flask)**
   - Serves the application on localhost
   - Handles recording requests
   - Displays emotion reports

2. **Emotion Detection Engine**
   - Uses OpenCV for video capture
   - Employs FER (Facial Emotion Recognition) for emotion detection
   - Runs in a separate thread to prevent UI blocking

3. **Storage System**
   - Captures stored in `static/captures/`
   - Automatic cleanup system for old captures

### Project Structure 

├── emotion_tracker.py      # Main application file
├── housekeeping.py        # Cleanup and report generation
├── templates/              # HTML templates
│   ├── index.html          # Main page layout
│   └── report.html         # Emotion report page
├── static/                 # Static files (images, etc.)
│   ├── captures/           # Captured frames
│   └── report.css          # CSS for report page
## Setup and Installation

**Create Virtual Environment**

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

pip install flask opencv-python fer pillow

3. **Create Required Directories**

mkdir -p static/captures
mkdir templates


4. **Run the Application**
python emotion_tracker.py


5. **Access the Application**
- Open browser
- Navigate to `http://localhost:5000`

## Lessons Learned & Troubleshooting Guide

### 1. Camera Access Issues

**Problem:** Camera not accessible or returning blank frames

**Solution:**
- Ensure camera is connected and functioning correctly.
- Check device manager for any driver issues.
- Test with a different browser or machine to rule out browser/machine-specific issues.

ret is False or frame is None

**Solutions:**
- Ensure no other application is using the camera
- Check camera permissions for Python/application
- Try different camera index (0, 1, etc.) if multiple cameras exist

**Prevention:**
- Add camera availability check before starting recording
- Implement graceful fallback if camera is unavailable

### 2. Threading Issues

**Problem:** UI freezing during recording

**Solution:** Implemented threading for emotion detection


**Prevention:**
- Always run long-running tasks in separate threads
- Use thread-safe variables for shared data
- Implement proper thread cleanup

### 3. File System Management

**Problem:** Accumulating capture files consuming disk space

**Solution:** Created housekeeping script to clean old files



**Prevention:**
- Implement automatic cleanup
- Use structured file naming
- Monitor storage usage

### 4. Memory Management

**Problem:** Memory usage growing with continuous use

**Solutions:**
- Properly release camera resources
- Clean up image arrays
- Implement garbage collection

**Prevention:**

### 5. Browser Compatibility

**Problem:** Different behaviors across browsers

**Solution:** 
- Standardized JavaScript code
- Added browser-specific checks
- Implemented polling for status updates

**Prevention:**
- Test across multiple browsers
- Use standard Web APIs
- Implement graceful degradation

## Performance Optimization Tips

1. **Image Processing**
   - Resize frames before processing
   - Implement frame rate limiting
   - Use appropriate image formats

2. **Storage Management**
   - Regular cleanup of old files
   - Compress images when possible
   - Monitor disk usage

3. **Memory Usage**
   - Clear variables when not needed
   - Use generators for large datasets
   - Implement proper resource cleanup

## Future Improvements

1. **Features**
   - Add emotion intensity tracking
   - Implement multi-face detection
   - Add video export capability

2. **Technical**
   - Implement WebSocket for real-time updates
   - Add database storage option
   - Improve error handling and recovery

3. **UI/UX**
   - Add progress indicator
   - Implement responsive design
   - Add dark mode support

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.