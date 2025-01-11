


Python version 3.13.1

source xxx

pip install opencv-python
pip install dlib


确保电脑安装了ffmpeg





git clone xxx
cd xxxxx
cp dailyPhoto.plist ${HOME}/Library/LaunchAgents/
launchctl load ${HOME}/Library/LaunchAgents/dailyPhoto.plist



摄像头的权限问题
- 赋权给ffmpeg
- 赋权给terminal


每天的10、14、16、20、23点运行，可在 `dailyPhoto.plist的StartCalendarInterval` 中根据实际情况自行调整运行时间