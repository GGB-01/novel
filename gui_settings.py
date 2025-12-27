# gui_settings.py - 设置窗口GUI
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, END


class SettingsWindow:
    """系统设置窗口"""

    def __init__(self, config, utils):
        self.config = config
        self.utils = utils
        self.window = None
        self.text_log = None

    def create_window(self) -> None:
        """创建系统设置窗口"""
        self.window = tk.Toplevel()
        self.window.title("系统设置 - 配置界面")
        self.window.geometry("700x500")
        self.window.resizable(True, True)

        main_frame = ttk.Frame(self.window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self._create_path_settings(main_frame)
        self._create_log_settings(main_frame)

        self._load_log()
        self.utils.center_window(self.window)

    def _create_path_settings(self, parent: ttk.Frame) -> None:
        """创建路径设置区域"""
        path_frame = ttk.LabelFrame(parent, text="保存路径设置", padding="10")
        path_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(path_frame, text="保存路径：").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.entry_path = ttk.Entry(path_frame)
        self.entry_path.grid(row=0, column=1, sticky=tk.EW, padx=(0, 10))
        self.entry_path.insert(0, self.config.save_path)
        path_frame.columnconfigure(1, weight=1)

        btn_path = ttk.Button(path_frame, text="选择路径", width=10,
                              command=self._select_save_path)
        btn_path.grid(row=0, column=2)

    def _create_log_settings(self, parent: ttk.Frame) -> None:
        """创建日志设置区域"""
        log_frame = ttk.LabelFrame(parent, text="系统日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True)

        self.text_log = scrolledtext.ScrolledText(log_frame, font=("Consolas", 9),
                                                  wrap=tk.WORD)
        self.text_log.pack(fill=tk.BOTH, expand=True)

        # 按钮区域
        button_frame = ttk.Frame(log_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))

        btn_export_log = ttk.Button(button_frame, text="导出日志",
                                    command=self._export_log)
        btn_export_log.pack(side=tk.RIGHT, padx=(5, 0))

        btn_clear_log = ttk.Button(button_frame, text="清空日志",
                                   command=self._clear_log)
        btn_clear_log.pack(side=tk.RIGHT)

    def _select_save_path(self) -> None:
        """选择保存路径"""
        folder = filedialog.askdirectory(title="选择保存目录")
        if folder:
            self.config.set_save_path(folder)
            self.entry_path.delete(0, END)
            self.entry_path.insert(0, self.config.save_path)
            messagebox.showinfo("成功", f"保存路径已设置为：\n{self.config.save_path}")

    def _load_log(self) -> None:
        """加载日志"""
        self.text_log.delete(1.0, tk.END)
        for message in self.config.global_log:
            self.text_log.insert(tk.END, message + "\n")
        self.text_log.see(tk.END)

    def _clear_log(self) -> None:
        """清除日志"""
        self.config.global_log.clear()
        self.text_log.delete(1.0, tk.END)
        messagebox.showinfo("成功", "系统日志已清空")

    def _export_log(self) -> None:
        """导出日志"""
        if not self.config.global_log:
            messagebox.showwarning("提示", "系统日志为空，无需导出")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存日志文件",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(self.config.global_log))
                messagebox.showinfo("成功", f"日志已导出到：\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"日志导出失败：{str(e)}")