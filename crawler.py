# crawler.py - 爬虫核心功能
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse
from typing import List, Dict, Optional
import tkinter as tk
from tkinter import scrolledtext

# 屏蔽SSL警告
try:
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    pass


class NovelCrawler:
    """小说爬取类"""

    def __init__(self, config, utils):
        self.config = config
        self.utils = utils

    def get_page_data(self, page_num: int, keyword_encoded: str) -> List[Dict]:
        """获取单页小说数据"""
        page_params = self.config.PARAMS.copy()
        page_params["kw"] = keyword_encoded
        if page_num > 1:
            page_params["p"] = page_num

        try:
            response = requests.get(
                url=self.config.BASE_URL,
                params=page_params,
                headers=self.config.HEADERS,
                timeout=30,
                verify=False
            )
            response.raise_for_status()
            response.encoding = "gbk"

            soup = BeautifulSoup(response.text, "html.parser")
            page_data = []

            for h3_tag in soup.find_all("h3", class_="title"):
                a_tag = h3_tag.find("a", href=True)
                if not a_tag:
                    continue

                novel_name = a_tag.get_text(strip=True)
                href = a_tag["href"].strip()
                if not href.startswith("http"):
                    href = urllib.parse.urljoin(self.config.BASE_URL, href)

                novel_id = self.utils.extract_novel_id(href)
                page_data.append({
                    "名称": novel_name,
                    "链接": href,
                    "novelid": novel_id
                })

            return page_data
        except Exception as e:
            return []

    def crawl_novels(self, keyword: str, max_novels: int,
                     crawl_until_fail: bool,
                     log_widget: Optional[scrolledtext.ScrolledText] = None) -> List[Dict]:
        """爬取小说列表"""
        all_data = []
        seen_links = set()
        page_num = 1
        empty_page_count = 0
        max_empty_pages = 2

        keyword_encoded = self.utils.encode_keyword(keyword)
        if not keyword_encoded:
            return []

        self.utils.log_message(f"开始爬取关键词「{keyword}」的小说数据...", self.config, log_widget)

        if crawl_until_fail:
            self.utils.log_message(f"爬取模式：爬取直到连续3页为空", self.config, log_widget)
        else:
            self.utils.log_message(f"爬取模式：最多{max_novels}条（连续{max_empty_pages}页空则终止）", self.config,
                                   log_widget)

        while True:
            if page_num > 50:
                self.utils.log_message(f"⚠️ 已爬取50页，强制终止", self.config, log_widget)
                break

            self.utils.log_message(f"正在爬取第{page_num}页...（当前已获取{len(all_data)}条）", self.config, log_widget)

            page_data = self.get_page_data(page_num, keyword_encoded)

            if not page_data:
                empty_page_count += 1
                self.utils.log_message(f"❌ 第{page_num}页无数据（连续空页{empty_page_count}次）", self.config, log_widget)

                if crawl_until_fail and empty_page_count >= 3:
                    self.utils.log_message(f"⚠️ 连续3页为空，终止爬取", self.config, log_widget)
                    break
                elif not crawl_until_fail and empty_page_count >= max_empty_pages:
                    self.utils.log_message(f"⚠️ 连续{max_empty_pages}页为空，终止爬取", self.config, log_widget)
                    break
            else:
                empty_page_count = 0
                new_count = 0

                for item in page_data:
                    if item["链接"] not in seen_links:
                        seen_links.add(item["链接"])
                        all_data.append(item)
                        new_count += 1

                        if not crawl_until_fail and len(all_data) >= max_novels:
                            all_data = all_data[:max_novels]
                            self.utils.log_message(f"✅ 已获取{max_novels}条数据，达到数量限制", self.config, log_widget)
                            break

                self.utils.log_message(f"✅ 第{page_num}页爬取完成，新增{new_count}条（累计{len(all_data)}条）",
                                       self.config, log_widget)

                if not crawl_until_fail and len(all_data) >= max_novels:
                    break

            self.utils.log_message(f"等待2秒后继续...", self.config, log_widget)
            time.sleep(2)
            page_num += 1

        self.utils.log_message(f"\n========== 爬取完成 ==========", self.config, log_widget)
        self.utils.log_message(f"最终获取到 {len(all_data)} 本小说", self.config, log_widget)

        self.config.novel_data_list = all_data
        return all_data