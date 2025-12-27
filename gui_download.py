# gui_download.py - 下载窗口GUI
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, Listbox, END
import threading
from downloader import NovelDownloader


class DownloadWindow:
    """下载管理窗口"""

    def __init__(self, config, utils):
        self.config = config
        self.utils = utils
        self.downloader = NovelDownloader(config, utils)
        self.window = None
        self.listbox_novels = None
        self.text_log = None

    def create_window(self) -> None:
        """创建下载管理窗口"""
        self.window = tk.Toplevel()
        self.window.title("小说下载 - 管理界面")
        self.window.geometry("800x600")
        self.window.resizable(True, True)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_config_area(main_frame)
        self._create_novel_list_area(main_frame)
        self._create_log_area(main_frame)

        self._update_novel_list()
        self.utils.center_window(self.window)

    def _create_config_area(self, parent: ttk.Frame) -> None:
        """创建配置区域"""
        config_frame = ttk.LabelFrame(parent, text="下载配置", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(config_frame, text="开始章节：").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_start_chapter = ttk.Entry(config_frame, width=10)
        self.entry_start_chapter.grid(row=0, column=1, padx=(0, 15))
        self.entry_start_chapter.insert(0, "1")

        ttk.Label(config_frame, text="结束章节：").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.entry_end_chapter = ttk.Entry(config_frame, width=10)
        self.entry_end_chapter.grid(row=0, column=3, padx=(0, 15))

        ttk.Label(config_frame, text="（留空下载全部）", foreground="gray").grid(row=0, column=4, sticky=tk.W)

        btn_download = ttk.Button(config_frame, text="下载选中小说", width=12,
                                  command=self._start_download)
        btn_download.grid(row=0, column=5, padx=(15, 0))

        btn_refresh = ttk.Button(config_frame, text="刷新列表", width=10,
                                 command=self._update_novel_list)
        btn_refresh.grid(row=0, column=6)

    def _create_novel_list_area(self, parent: ttk.Frame) -> None:
        """创建小说列表区域"""
        list_frame = ttk.LabelFrame(parent, text="可用小说", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.listbox_novels = Listbox(list_frame, font=("微软雅黑", 9))
        self.listbox_novels.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self.listbox_novels.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_novels.config(yscrollcommand=scrollbar.set)

    def _create_log_area(self, parent: ttk.Frame) -> None:
        """创建日志区域"""
        log_frame = ttk.LabelFrame(parent, text="下载日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.text_log = scrolledtext.ScrolledText(log_frame, font=("Consolas", 9),
                                                  wrap=tk.WORD, height=15)
        self.text_log.pack(fill=tk.BOTH, expand=True)

    def _update_novel_list(self) -> None:
        """更新小说列表"""
        self.listbox_novels.delete(0, END)
        if not self.config.novel_data_list:
            self.listbox_novels.insert(END, "（暂无小说数据，请先爬取）")
        else:
            for i, novel in enumerate(self.config.novel_data_list, 1):
                self.listbox_novels.insert(END, f"{i}. {novel['名称']}")

    def _start_download(self) -> None:
        """开始下载"""
        selected = self.listbox_novels.curselection()
        if not selected or not self.config.novel_data_list:
            messagebox.showwarning("提示", "请先选择要下载的小说！")
            return

        idx = selected[0]
        if idx >= len(self.config.novel_data_list):
            messagebox.showerror("错误", "选中的小说不存在！")
            return

        novel = self.config.novel_data_list[idx]
        novel_id = novel["novelid"]
        novel_name = novel["名称"]

        try:
            start_chapter = int(self.entry_start_chapter.get().strip()) if self.entry_start_chapter.get().strip() else 1
            end_chapter = int(self.entry_end_chapter.get().strip()) if self.entry_end_chapter.get().strip() else 0
        except ValueError:
            messagebox.showerror("错误", "章节号必须是数字！")
            return

        self.text_log.delete(1.0, tk.END)

        def download_thread():
            try:
                self.downloader.download_novel_chapters(novel_id, novel_name,
                                                        start_chapter, end_chapter,
                                                        self.text_log)
            except Exception as e:
                self.utils.log_message(f"\n❌ 下载出错：{str(e)}", self.config, self.text_log)
                messagebox.showerror("错误", f"下载失败：{str(e)}")

        threading.Thread(target=download_thread, daemon=True).start()