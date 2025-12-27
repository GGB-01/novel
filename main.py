# main.py - 主程序入口
from gui_main import MainWindow

def main():
    """主函数"""
    app = MainWindow()
    root = app.create_window()
    root.mainloop()

if __name__ == "__main__":
    main()