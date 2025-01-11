
本项目是利用电脑前摄像头拍摄每日无意识时的工作状态，即在电脑前工作时会拍摄一张照片。

注意事项
- 本人的Python版本 3.13.1
- 摄像头的权限赋权给ffmpeg、terminal
- 确保安装了ffmpeg，并且其路径在 `dailyPhoto.plist` 文件下的 `EnvironmentVariables-->PATH` 中
- 目前只有macos版本， 如果windows需要的伙伴可以自行参考开发。



```
cd $HOME
git clone xxx
cd ./DailyPhoto
cp dailyPhoto.plist ${HOME}/Library/LaunchAgents/



python3 -m venv dailyPhotoVenv
source ./dailyPhotoVenv/bin/activate
pip3 install -r requirements.txt
```


```
launchctl load ${HOME}/Library/LaunchAgents/dailyPhoto.plist
```




大体讲解
- 每天的10、14、16、20、23点运行，可在 `dailyPhoto.plist文件的StartCalendarInterval字段` 中根据实际情况自行调整运行时间
- 若上述时间段某一次拍摄到了人脸，则不会继续拍摄
- 具体逻辑 请参考 `main.py` 文件


