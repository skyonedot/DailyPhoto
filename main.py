#!/usr/bin/env python3

import cv2
import os
from datetime import datetime
import dlib
from pathlib import Path
import subprocess
import re

class DailyPhotoCapture:
    """
    A class to automatically capture daily photos with face detection.
    This tool uses ffmpeg to capture photos and dlib for face detection.
    """

    def __init__(self):
        # Get user's home directory
        home_dir = str(Path.home())
        
        # Set up directory structure
        self.base_dir = os.path.join(home_dir, "Pictures", "DailyPhoto")
        self.photos_dir = os.path.join(self.base_dir, "Photos")
        
        # Create directories if they don't exist
        os.makedirs(self.photos_dir, exist_ok=True)
        
        # Set up file paths
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.photo_path = os.path.join(self.photos_dir, f"{self.current_date}.png")
        self.log_path = os.path.join(self.base_dir, "daily_capture.log")
        
        # Add screenshot directory
        self.screenshots_dir = os.path.join(self.base_dir, "Screenshots")
        os.makedirs(self.screenshots_dir, exist_ok=True)


    def capture_photo(self):
        """
        Capture a photo using ffmpeg through the system's default camera.
        Uses high quality settings for better face detection.
        """
        command = (
            "ffmpeg -f avfoundation -pixel_format uyvy422 -framerate 30 "
            "-video_size 1920x1080 -i '0' -vframes 1 -loglevel error {}"
        ).format(self.photo_path)
        os.system(command)

    def detect_face(self):
        """
        Detect faces in the captured photo using dlib's face detector.
        
        Returns:
            bool: True if at least one face is detected, False otherwise
        """
        try:
            image = cv2.imread(self.photo_path)
            if image is None:
                print(f"Error: Unable to load image from {self.photo_path}")
                return False
            
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            face_detector = dlib.get_frontal_face_detector()
            faces = face_detector(gray_image, 2)  # Upsample 2 times for better detection
            
            return len(faces) > 0
            
        except Exception as e:
            print(f"Face detection error: {e}")
            return False

    def get_display_count(self):
        """
        Get the number of connected displays
        """
        command = ["system_profiler", "SPDisplaysDataType"]
        output = subprocess.check_output(command, text=True)
        return len(re.findall(r"Resolution", output))

    def capture_screenshots(self):
        """
        Capture screenshots from all connected displays and save as PDF
        Returns:
            list: Paths to captured screenshot files
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        display_count = self.get_display_count()
        capture_files = []
        
        for i in range(1, display_count + 1):
            file_path = os.path.join(self.screenshots_dir, f"screen_{self.current_date}_{i}.pdf")
            capture_files.append(file_path)
        
        capture_command = ["screencapture", "-x", "-t", "pdf"] + capture_files
        subprocess.run(capture_command, check=True)
        return capture_files

    def run(self):
        """
        Main execution flow:
        1. Check if photo already exists for today
        2. Capture new photo and screenshots if needed
        3. Verify face presence
        4. Keep or delete photo based on face detection
        """
        if os.path.exists(self.photo_path):
            print(f"Today's photo already exists: {self.photo_path}")
            return

        print(f"Capturing new photo: {self.photo_path}")
        self.capture_photo()
        
        print("Capturing screenshots...")
        try:
            screenshot_files = self.capture_screenshots()
            print(f"Screenshots saved: {len(screenshot_files)} displays captured")
        except Exception as e:
            print(f"Error capturing screenshots: {e}")
        
        if self.detect_face():
            print("Face detected - photo saved successfully")
        else:
            print("No face detected - deleting photo")
            os.remove(self.photo_path)
            for screenshot in screenshot_files:
                if os.path.exists(screenshot):
                    os.remove(screenshot)


if __name__ == "__main__":
    DailyPhotoCapture().run()