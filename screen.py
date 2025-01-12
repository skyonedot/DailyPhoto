import os
import subprocess
import datetime
import re


def is_screen_locked():
    """
    检查屏幕是否锁定（仅支持 macOS）
    """
    try:
        command = [
            "/usr/libexec/PlistBuddy",
            "-c",
            "print :IOConsoleUsers:0:CGSSessionScreenIsLocked",
            "/dev/stdin",
        ]
        ioreg_output = subprocess.check_output(
            ["ioreg", "-n", "Root", "-d1", "-a"], text=True
        )
        result = subprocess.check_output(command, input=ioreg_output, text=True).strip()
        return result == "true"
    except subprocess.CalledProcessError:
        return False


def get_display_count():
    """
    获取显示器的数量
    """
    command = ["system_profiler", "SPDisplaysDataType"]
    output = subprocess.check_output(command, text=True)
    return len(re.findall(r"Resolution", output))


def capture_screenshots(output_path, timestamp, display_count):
    """
    截屏并保存为 PDF
    """
    capture_files = []
    for i in range(1, display_count + 1):
        file_path = os.path.join(output_path, f"capture.{timestamp}.{i}.pdf")
        capture_files.append(file_path)
    
    capture_command = ["screencapture", "-x", "-t", "pdf"] + capture_files
    subprocess.run(capture_command, check=True)
    return capture_files


def run_ocr(capture_files, ocr_tool_path):
    """
    对截图 PDF 文件执行 OCR
    """
    for file_path in capture_files:
        subprocess.run(
            [
                "taskpolicy",
                "-b",
                ocr_tool_path,
                file_path,
                file_path,
                "-l",
                "chi_sim+eng",
                "--output-type",
                "pdf",
                "--optimize",
                "3",
            ],
            check=True,
        )


def main():
    if not is_screen_locked():
        # 准备输出目录和时间戳
        output_path = os.path.expanduser("~/Pictures/Rewind")
        os.makedirs(output_path, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # 检测 OCR 工具是否可用
        ocr_tool_path = subprocess.run(
            ["command", "-v", "ocrmypdf"], capture_output=True, text=True
        ).stdout.strip()
        if not ocr_tool_path:
            print("ocrmypdf could not be found")
            return

        # 获取显示器数量
        display_count = get_display_count()
        print(f"Detected {display_count} displays.")

        # 截屏
        print(f"Capturing at {timestamp}")
        try:
            capture_files = capture_screenshots(output_path, timestamp, display_count)
            print("Screenshots captured.")
        except Exception as e:
            print(f"Error during screenshot capture: {e}")
            return

        # # 执行 OCR
        # try:
        #     run_ocr(capture_files, ocr_tool_path)
        #     print("OCR processing completed.")
        # except Exception as e:
        #     print(f"Error during OCR processing: {e}")


if __name__ == "__main__":
    main()
