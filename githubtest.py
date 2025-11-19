import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os, subprocess, sys

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

class GUIWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('无语专用py文件加密工具')
        self.geometry('500x200')
        self.resizable(width=False, height=False)
        self.init_ui()
        self.is_file = False


    def init_ui(self):
        center_frame = tk.Frame(self)
        center_frame.grid(row=0, column=0)

        # 将所有组件放在这个框架内
        self.label = tk.Label(center_frame, text='选择要加密的py文件:')
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.path_var = tk.StringVar()
        self.path_entry = ttk.Entry(center_frame, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=1)

        self.browse_button = ttk.Button(center_frame, text='浏览文件夹', command=self.browse_folder)
        self.browse_button.grid(row=0, column=2)
        self.browse_file_button = ttk.Button(center_frame, text='浏览py文件', command=self.browse_files)
        self.browse_file_button.grid(row=0, column=3)

        self.confirm_button = tk.Button(self, text='确认加密', command=self.batch_encrypt_py_files)
        self.confirm_button.grid(row=1, column=1, padx=15, pady=5)

        # 让整个框架在窗口中居中
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_columnconfigure(1, weight=1)


    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_var.set(folder_path)
            self.is_file = False


    def browse_files(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Python files", "*.py")]
        )
        if file_path:
            self.path_var.set(file_path)
            self.is_file = True


    def batch_encrypt_py_files(self):
        folder_path = self.path_var.get()
        folder_path = os.path.join(BASE_DIR, folder_path)
        if not folder_path:
            messagebox.showinfo('错误提示', "请先选择文件夹")
            return
        if not self.is_file:
            is_py = False
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        # 调用你的加密函数
                        self.encrypt_file_to_pyd(file_path)
                        is_py = True
            if not is_py:
                messagebox.showinfo('错误提示', "未找到py文件")
        elif self.is_file:
            print(folder_path)
            self.encrypt_file_to_pyd(folder_path)

    def encrypt_file_to_pyd(self, file_path):
        try:
            # 查找 PyArmor 可执行文件的完整路径
            import shutil

            # 查找 pyarmor 命令的完整路径
            pyarmor_path = shutil.which('pyarmor')
            if not pyarmor_path:
                # 如果在 PATH 中找不到，尝试在虚拟环境目录中查找
                venv_scripts = os.path.join('.venv', 'Scripts', 'pyarmor.exe')
                if os.path.exists(venv_scripts):
                    pyarmor_path = venv_scripts
                else:
                    messagebox.showerror('错误', "找不到 PyArmor 可执行文件")
                    return

            output_dir = os.path.join(os.path.dirname(file_path), 'encrypted')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 使用完整路径执行 PyArmor
            result = subprocess.run([
                pyarmor_path, 'gen',
                '-O', output_dir,
                file_path
            ], check=True, capture_output=True, text=True)

            messagebox.showinfo('成功', f"文件 {os.path.basename(file_path)} 加密成功，输出到：{output_dir}")

        except subprocess.CalledProcessError as e:
            error_msg = f"加密失败: {str(e)}\n"
            if e.stderr:
                error_msg += f"错误详情: {e.stderr}"
            messagebox.showerror('错误', error_msg)
        except Exception as e:
            messagebox.showerror('错误', f"发生未知错误: {str(e)}")

if __name__ == '__main__':
    window = GUIWindow()

    window.mainloop()
