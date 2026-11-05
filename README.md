# AirMouse

Control your Mac cursor by tracking an object such as an AirPods case using your webcam.

## Features
- Webcam object tracking with OpenCV
- Manual object selection
- M toggles mouse control
- Q quits the application
- PyAutoGUI failsafe enabled

## Requirements
- macOS
- Python 3
- Webcam

## Installation
1. Create environment: python3 -m venv venv
2. Activate: source venv/bin/activate
3. Install: pip install -r requirements.txt

## Run
python airmouse.py

Select the object, press M to enable cursor movement, and Q to quit.

Camera processing is local; video is not uploaded.
