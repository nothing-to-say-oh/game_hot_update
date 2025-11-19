import requests, sys, os
from urllib.parse import urlparse
import posixpath

UPDATE_URL = 'http://api.79safe.com/?Z9V5W7F2R6H8H0I3'
HEADERS = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0"
        }


# 获取更新链接的api接口
def get_url():
    response = requests.post(UPDATE_URL, headers=HEADERS, allow_redirects=True)
    return response.text


URL = get_url()


if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

    # 添加可能的模块路径
    possible_paths = [
        os.path.join(base_path, "pyautogui"),
        os.path.join(base_path, "pyscreeze"),
        os.path.join(base_path, "win32com"),
        os.path.join(base_path, "site-packages")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            sys.path.append(path)
            print(f"添加路径: {path}")

# 解决打包后路径问题
if getattr(sys, 'frozen', False):
    # 打包后的路径
    BASE_DIR = os.path.dirname(sys.executable)
    BASE_DIR = f"{BASE_DIR}\_internal"
    # 添加 DLL 目录到系统路径
    os.environ['PATH'] = BASE_DIR + os.pathsep + os.environ['PATH']
else:
    # 开发环境路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 添加到系统路径
sys.path.append(BASE_DIR)


def download_files():
    try:
        update_folder = os.path.join(BASE_DIR, "update")
        os.makedirs(update_folder, exist_ok=True)
        response = requests.get(URL,headers=HEADERS, allow_redirects=True)
        file_name = os.path.join(update_folder, get_file_name())
        with open(file_name, "wb") as f:
            f.write(response.content)
        print('文件下载完成')
    except requests.exceptions.RequestException as e:
    # 捕获所有网络相关错误：超时、连接失败、404/500 状态码、SSL 错误等
        print(f"网络错误：{str(e)}")
    except OSError as e:
    # 捕获文件系统相关错误：创建文件夹失败（权限不足）、写入文件失败（磁盘满/被占用）等
        print(f"文件操作错误：{str(e)}")
    except Exception as e:
        # 兜底捕获所有其他未预料到的错误（比如 get_file_name() 内部报错）
        print(f"未知错误：{str(e)}")


def get_file_name():
    parsed_url = urlparse(URL)
    filename = posixpath.basename(parsed_url.path)
    return filename


download_files()