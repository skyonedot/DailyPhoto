# Daily Photo Capture

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)

Daily Photo Capture is an automated tool that captures both webcam photos and screenshots at specified times throughout the day. It uses face detection to ensure that only photos containing people are saved, making it perfect for tracking your daily work patterns or creating time-lapse records of your workday.

## Features

- 🎯 Automated photo capture at scheduled times
- 👤 Face detection to ensure meaningful captures
- 🗑️ Automatic cleanup of photos without faces
- 📅 Organized storage with date-based naming
- 🔒 Privacy-focused (all data stored locally)

## Prerequisites

- macOS
- Python 3.13 or higher
- ffmpeg (for photo capture), and it's path contains in `dailyPhoto.plist` --> `EnvironmentVariables-->PATH` 
- Webcam access permissions for Terminal and ffmpeg
- change ${PATH} in `dailyPhoto.plist` as your reality. 🚩🚩🚩🚩




## Installation

1. Clone the repository:
```bash
cd ~/Applications
git clone https://github.com/skyonedot/DailyPhoto.git
cd DailyPhoto
```

2. Create and activate virtual environment:
```bash
python3 -m venv ~/.virtualenvs/DailyPhoto
source ~/.virtualenvs/DailyPhoto/bin/activate
```

3. Install dependencies:
```bash
pip3 install -r requirements.txt
```


4. Install and load the LaunchAgent:
```bash
cp dailyPhoto.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/dailyPhoto.plist
```



## Key Points

- The program runs at scheduled times (10:00, 14:00, 16:00, 20:00, and 23:00 by default). You can adjust these times in the `StartCalendarInterval` field of the `dailyPhoto.plist` file.
- If a face is detected in any photo during these time slots, the program will skip the remaining captures for that day.
- For detailed implementation logic, please refer to the `main.py` file.
- All successfully captured photos are saved in the `~/Pictures/DailyPhoto/Photos` directory, organized by date.
- All successfully screen shot are saved in the `~/Pictures/DailyPhoto/Photos` directory, organized by date.
- Both output logs and error logs are located in the `~/Pictures/DailyPhoto/Screenshots` directory.
- Currently, this program only runs on Macos. For Windows users, you're welcome to develop and customize your own version.
- For any issues or questions, please open an issue on GitHub. Pull requests are always welcome!