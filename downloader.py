# downloader.py - 下载器核心功能
import os
import time
import requests
from bs4 import BeautifulSoup
from typing import Optional
import tkinter as tk
from tkinter import scrolledtext, messagebox

# 屏蔽SSL警告
try:
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass


class NovelDownloader:
    """小说下载类"""

    def __init__(self, config, utils):
        self.config = config
        self.utils = utils

    def download_novel_chapters(self, novel_id: str, novel_name: str,
                                start_chapter: int, end_chapter: int,
                                log_widget: Optional[scrolledtext.ScrolledText] = None) -> None:
        """下载小说章节"""
        if not novel_id:
            messagebox.showerror("错误", "小说ID为空，无法下载！")
            return

        if start_chapter < 1:
            start_chapter = 1
            self.utils.log_message("⚠️ 开始章节不能小于1，自动设为1", self.config, log_widget)

        safe_name = self.utils.safe_filename(novel_name)
        save_dir = os.path.join(self.config.save_path, safe_name)
        os.makedirs(save_dir, exist_ok=True)

        chapter_id = start_chapter
        fail_count = 0
        total_downloaded = 0

        self.utils.log_message(f"\n========== 开始下载《{novel_name}》 ==========", self.config, log_widget)
        self.utils.log_message(f"保存路径：{save_dir}", self.config, log_widget)

        if end_chapter > 0:
            self.utils.log_message(f"下载范围：第{start_chapter}-{end_chapter}章", self.config, log_widget)
        else:
            self.utils.log_message(f"下载范围：第{start_chapter}章到最后一章", self.config, log_widget)

        while fail_count < 3:
            if end_chapter > 0 and chapter_id > end_chapter:
                break

            try:
                chapter_url = f"https://www.jjwxc.net/onebook.php?novelid={novel_id}&chapterid={chapter_id}"
                response = requests.get(chapter_url, headers=self.config.HEADERS,
                                        timeout=10, verify=False)

                if response.status_code != 200:
                    fail_count += 1
                    self.utils.log_message(f"❌ 第{chapter_id}章下载失败（状态码：{response.status_code}）", self.config,
                                           log_widget)
                    chapter_id += 1
                    time.sleep(1)
                    continue

                response.encoding = response.apparent_encoding or "gbk"
                soup = BeautifulSoup(response.text, "html.parser")
                novel_body = soup.find("div", class_="novelbody")

                if not novel_body:
                    fail_count += 1
                    self.utils.log_message(f"❌ 第{chapter_id}章无内容", self.config, log_widget)
                    chapter_id += 1
                    time.sleep(1)
                    continue

                chapter_title = soup.find("h2").get_text(strip=True) if soup.find("h2") else f"第{chapter_id}章"
                chapter_content = novel_body.get_text(separator="\n", strip=True)

                chapter_file = os.path.join(
                    save_dir,
                    f"{chapter_id}_{chapter_title.replace('/', '_').replace('\\', '_')}.txt"
                )

                with open(chapter_file, "w", encoding="utf-8") as f:
                    f.write(f"{chapter_title}\n\n{chapter_content}")

                fail_count = 0
                total_downloaded += 1
                self.utils.log_message(f"✅ 第{chapter_id}章下载成功：{chapter_title}", self.config, log_widget)

                chapter_id += 1
                time.sleep(1.5)

            except Exception as e:
                fail_count += 1
                self.utils.log_message(f"❌ 第{chapter_id}章下载异常：{str(e)}", self.config, log_widget)
                chapter_id += 1
                time.sleep(2)
                continue

        self.utils.log_message(f"\n========== 下载完成 ==========", self.config, log_widget)
        self.utils.log_message(f"共成功下载 {total_downloaded} 章", self.config, log_widget)
        self.utils.log_message(f"文件保存至：{save_dir}", self.config, log_widget)

        messagebox.showinfo(
            "完成",
            f"《{novel_name}》下载完成！\n共下载 {total_downloaded} 章\n保存路径：{save_dir}"
        )