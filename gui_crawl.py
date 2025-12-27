# gui_crawl.py - 爬取窗口GUI
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Listbox, END
import threading
from crawler import NovelCrawler


class CrawlWindow:
    """爬取配置窗口"""

    def __init__(self, config, utils):
        self.config = config
        self.utils = utils
        self.crawler = NovelCrawler(config, utils)
        self.window = None
        self.listbox_novels = None
        self.text_log = None

    def create_window(self) -> None:
        """创建爬取配置窗口"""
        self.window = tk.Toplevel()
        self.window.title("小说爬取 - 配置界面")
        self.window.geometry("800x600")
        self.window.resizable(True, True)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_config_area(main_frame)
        self._create_result_area(main_frame)
        self._create_log_area(main_frame)

        self.utils.center_window(self.window)

    def _create_config_area(self, parent: ttk.Frame) -> None:
        """创建配置区域"""
        config_frame = ttk.LabelFrame(parent, text="爬取配置", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(config_frame, text="搜索关键词：").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_keyword = ttk.Entry(config_frame, width=30)
        self.entry_keyword.grid(row=0, column=1, padx=(0, 15))

        ttk.Label(config_frame, text="最大爬取数量：").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.entry_max_novels = ttk.Entry(config_frame, width=10)
        self.entry_max_novels.grid(row=0, column=3, padx=(0, 15))
        self.entry_max_novels.insert(0, "50")

        self.var_crawl_until_fail = tk.BooleanVar(value=False)
        chk_until_fail = ttk.Checkbutton(config_frame, text="爬取直到失败",
                                         variable=self.var_crawl_until_fail)
        chk_until_fail.grid(row=0, column=4, padx=(0, 15))

        btn_crawl = ttk.Button(config_frame, text="开始爬取", width=12,
                               command=self._start_crawling)
        btn_crawl.grid(row=0, column=5)

    def _create_result_area(self, parent: ttk.Frame) -> None:
        """创建结果显示区域"""
        result_frame = ttk.LabelFrame(parent, text="爬取结果", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.listbox_novels = Listbox(result_frame, font=("微软雅黑", 9))
        self.listbox_novels.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    def _create_log_area(self, parent: ttk.Frame) -> None:
        """创建日志区域"""
        log_frame = ttk.LabelFrame(parent, text="爬取日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.text_log = scrolledtext.ScrolledText(log_frame, font=("Consolas", 9),
                                                  wrap=tk.WORD, height=15)
        self.text_log.pack(fill=tk.BOTH, expand=True)

    def _update_novel_list(self) -> None:
        """更新小说列表"""
        self.listbox_novels.delete(0, END)
        for i, novel in enumerate(self.config.novel_data_list, 1):
            self.listbox_novels.insert(END, f"{i}. {novel['名称']}")

    def _start_crawling(self) -> None:
        """开始爬取"""
        keyword = self.entry_keyword.get().strip()
        if not keyword:
            messagebox.showwarning("提示", "请输入搜索关键词！")
            return

        crawl_until_fail = self.var_crawl_until_fail.get()
        max_novels = 50

        if not crawl_until_fail:
            try:
                max_novels = int(self.entry_max_novels.get().strip())
                if max_novels < 1:
                    messagebox.showerror("错误", "爬取数量必须大于0！")
                    return
            except ValueError:
                messagebox.showerror("错误", "爬取数量必须是数字！")
                return

        self.text_log.delete(1.0, tk.END)
        self.listbox_novels.delete(0, END)

        def crawl_thread():
            try:
                self.crawler.crawl_novels(keyword, max_novels, crawl_until_fail, self.text_log)
                self.window.after(0, self._update_novel_list)
            except Exception as e:
                self.utils.log_message(f"\n❌ 爬取出错：{str(e)}", self.config, self.text_log)
                messagebox.showerror("错误", f"爬取失败：{str(e)}")

        threading.Thread(target=crawl_thread, daemon=True).start()