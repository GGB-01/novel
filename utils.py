# utils.py - 工具函数类
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox
from typing import Optional


class Utils:
    """工具类"""

    @staticmethod
    def extract_novel_id(url: str) -> str:
        """从小说链接中提取novelid"""
        try:
            match = re.search(r'novelid=(\d+)', url)
            return match.group(1) if match else ""
        except Exception:
            return ""

    @staticmethod
    def encode_keyword(keyword: str) -> str:
        """GB2312编码"""
        try:
            gb2312_bytes = keyword.encode('gb2312')
            encoded_parts = [f"%{b:02X}" for b in gb2312_bytes]
            return ''.join(encoded_parts)
        except Exception as e:
            messagebox.showerror("编码错误", f"关键词编码失败：{str(e)}")
            return ""

    @staticmethod
    def safe_filename(filename: str) -> str:
        """生成安全的文件名"""
        return re.sub(r'[\\/:*?"<>|]', '_', filename)

    @staticmethod
    def log_message(message: str, config, log_widget: Optional[scrolledtext.ScrolledText] = None) -> None:
        """记录日志消息"""
        config.global_log.append(message)
        if log_widget:
            log_widget.insert(tk.END, message + "\n")
            log_widget.see(tk.END)

    @staticmethod
    def center_window(window) -> None:
        """窗口居中显示"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")