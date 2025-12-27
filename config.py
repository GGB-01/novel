# config.py - 配置管理类
import os
from typing import List, Dict


class ConfigManager:
    """配置管理类"""

    # 基础配置
    BASE_URL = "https://www.jjwxc.net/search.php"

    PARAMS = {
        "kw": "",
        "ord": "",
        "t": "1"
    }

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Referer": "https://www.jjwxc.net/",
        "Host": "www.jjwxc.net",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    # 默认保存路径
    DEFAULT_SAVE_PATH = os.path.join(os.getcwd(), "小说下载")

    def __init__(self):
        self.novel_data_list: List[Dict] = []
        self.save_path: str = self.DEFAULT_SAVE_PATH
        self.global_log: List[str] = []

    def set_save_path(self, path: str) -> None:
        """设置保存路径"""
        self.save_path = path