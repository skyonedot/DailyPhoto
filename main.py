import cv2
import os
from datetime import datetime  # 仅导入 datetime 类
import dlib

# # 路径和配置
# 获取当前时间戳
# current_date = datetime.now().strftime("%Y-%m-%d_%H-%M")
current_date = datetime.now().strftime("%Y-%m-%d")

# current_date = 

# 生成带时间的照片保存路径
PHOTO_PATH = os.path.expanduser(f"/Users/skyone/Pictures/DailyPhoto/PNG/{current_date}.png")
LOG_PATH = os.path.expanduser("/Users/skyone/Pictures/DailyPhoto/PNG/daily_capture.log")  # 运行日志文件


# 检查今天是否已运行过,若PHOTO_PATH存在， 则今天已经运行，返回True
def already_ran_today():
    return True if os.path.exists(PHOTO_PATH) else False


# 检测图像中是否有人脸
def detect_face_in_image(image_path):
    """
    检测指定的图像中是否有人脸。
    
    :param image_path: 图像文件的路径（JPG格式）。
    :return: 如果检测到人脸返回 True，否则返回 False。
    """
    try:
        # 加载图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to load image from {image_path}")
            return False

        # 加载人脸检测模型
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        if face_cascade.empty():
            print("Error: Failed to load face detection model.")
            return False

        # 转换为灰度图
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = face_cascade.detectMultiScale(
            gray_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # 返回检测结果
        if len(faces) > 0:
            return True
        else:
            #print("No faces detected in the image.")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False




def detect_face_in_image2(image_path):
    """
    检测指定的图像中是否有人脸 (使用 dlib 深度学习模型)。
    
    :param image_path: 图像文件的路径（JPG格式）。
    :return: 如果检测到人脸返回 True，否则返回 False。
    """
    try:
        # 加载图像
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error: Unable to load image from {image_path}")
            return False

        # 转换为灰度图
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 加载 dlib 的人脸检测器
        face_detector = dlib.get_frontal_face_detector()

        # 检测人脸
        faces = face_detector(gray_image, 2)  # 第二个参数表示图像放大倍数，提高检测精度

        # 返回检测结果
        if len(faces) > 0:
            return True
        else:
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False


# 拍照
def capture_photo(PHOTO_PATH):
    os.system("ffmpeg -f avfoundation -pixel_format uyvy422 -framerate 30 -i '0' -vframes 1 -update 1 {}".format(PHOTO_PATH))


def capture_photo2(PHOTO_PATH):
    # 设置分辨率、帧率和像素格式
    command = (
        "ffmpeg -f avfoundation -pixel_format uyvy422 -framerate 30 "
        "-video_size 1920x1080 -i '0' -vframes 1 -loglevel error {}".format(PHOTO_PATH)
    )
    os.system(command)

#如果不包含人脸， 则删除图片
def del_photo(PHOTO_PATH):
    os.system("rm {}".format(PHOTO_PATH))
    
# # 主程序
if __name__ == "__main__":

    
    # print(detect_face_in_image2('/Users/skyone/Pictures/DailyPhoto/PNG/2025-01-07_21-21.png'))
    if already_ran_today():
        print("Today had already run.",PHOTO_PATH)
    else:
        print("Today path is,",PHOTO_PATH)
        capture_photo2(PHOTO_PATH)
        if detect_face_in_image2(PHOTO_PATH):
            print("Contain face. Success\n")
        else:
            print("No face. Delete photo.\n")
            del_photo(PHOTO_PATH)