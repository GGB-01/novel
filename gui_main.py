# gui_main.py - 主窗口GUI
import tkinter as tk
from tkinter import ttk
from gui_crawl import CrawlWindow
from gui_download import DownloadWindow
from gui_settings import SettingsWindow
from config import ConfigManager
from utils import Utils


class MainWindow:
    """主窗口类"""

    def __init__(self):
        self.root = None
        self.config = ConfigManager()
        self.utils = Utils()
        self.crawl_window_instance = None
        self.download_window_instance = None
        self.settings_window_instance = None

    def create_window(self) -> tk.Tk:
        """创建主窗口"""
        self.root = tk.Tk()
        self.root.title("小说爬虫工具 - 主界面")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        # 设置图标（可选）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass

        self._create_main_frame()
        self.utils.center_window(self.root)

        return self.root

    def _create_main_frame(self) -> None:
        """创建主框架"""
        main_frame = ttk.Frame(self.root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text="小说爬虫工具",
            font=("微软雅黑", 20, "bold"),
            foreground="#2c3e50"
        )
        title_label.pack(pady=(0, 40))

        # 功能按钮
        self._create_function_buttons(main_frame)

        # 底部信息
        self._create_footer(main_frame)

    def _create_function_buttons(self, parent: ttk.Frame) -> None:
        """创建功能按钮"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.BOTH, expand=True)

        # 爬取按钮
        btn_crawl = tk.Button(
            button_frame,
            text="小说爬取",
            font=("微软雅黑", 12),
            width=20,
            height=3,
            bg="#3498db",
            fg="white",
            relief=tk.RAISED,
            bd=3,
            command=self._open_crawl_window
        )
        btn_crawl.pack(pady=(0, 20))

        # 下载按钮
        btn_download = tk.Button(
            button_frame,
            text="下载管理",
            font=("微软雅黑", 12),
            width=20,
            height=3,
            bg="#2ecc71",
            fg="white",
            relief=tk.RAISED,
            bd=3,
            command=self._open_download_window
        )
        btn_download.pack(pady=(0, 20))

        # 设置按钮
        btn_settings = tk.Button(
            button_frame,
            text="系统设置",
            font=("微软雅黑", 12),
            width=20,
            height=3,
            bg="#f39c12",
            fg="white",
            relief=tk.RAISED,
            bd=3,
            command=self._open_settings_window
        )
        btn_settings.pack()

    def _create_footer(self, parent: ttk.Frame) -> None:
        """创建底部信息"""
        info_label = ttk.Label(
            parent,
            text="© 2025 小说爬虫工具 - 仅供学习使用",
            font=("微软雅黑", 10),
            foreground="#7f8c8d"
        )
        info_label.pack(side=tk.BOTTOM, pady=(20, 0))

    def _open_crawl_window(self) -> None:
        """打开爬取窗口"""
        if self.crawl_window_instance is None or not self.crawl_window_instance.window.winfo_exists():
            self.crawl_window_instance = CrawlWindow(self.config, self.utils)
            self.crawl_window_instance.create_window()

    def _open_download_window(self) -> None:
        """打开下载窗口"""
        if self.download_window_instance is None or not self.download_window_instance.window.winfo_exists():
            self.download_window_instance = DownloadWindow(self.config, self.utils)
            self.download_window_instance.create_window()

    def _open_settings_window(self) -> None:
        """打开设置窗口"""
        if self.settings_window_instance is None or not self.settings_window_instance.window.winfo_exists():
            self.settings_window_instance = SettingsWindow(self.config, self.utils)
            self.settings_window_instance.create_window()