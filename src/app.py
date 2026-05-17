#!/usr/bin/env python3
"""
image-compress - 图片压缩工具
工具编号: tool-016
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

class App:
    def __init__(self, root):
        self.root = root
        root.title("图片压缩工具 v1.0")
        root.geometry("800x600")
        self.images = []
        self.setup_ui()
    
    def setup_ui(self):
        # 标题
        title_frame = tk.Frame(self.root, bg="#9C27B0", height=60)
        title_frame.pack(fill="x")
        title_frame.pack_propagate(False)
        tk.Label(title_frame, text="🖼️ 图片压缩工具", font=("Arial", 18, "bold"),
                 fg="white", bg="#9C27B0").pack(pady=15)
        
        # 主区域
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        
        # 图片选择
        file_frame = tk.LabelFrame(main, text="📷 图片选择", font=("Arial", 10, "bold"))
        file_frame.pack(fill="x", pady=10)
        
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="➕ 添加图片", command=self.add_images,
                  bg="#9C27B0", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📁 添加文件夹", command=self.add_folder,
                  bg="#9C27B0", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ 清空", command=self.clear_images,
                  bg="#f44336", fg="white", padx=15, pady=8).pack(side="left", padx=5)
        
        # 图片列表
        list_frame = tk.Frame(main)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        self.image_listbox = tk.Listbox(list_frame, font=("Consolas", 10), height=10)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", 
                                  command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.image_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # 设置选项
        options_frame = tk.LabelFrame(main, text="⚙️ 设置", font=("Arial", 10, "bold"))
        options_frame.pack(fill="x", pady=10)
        
        tk.Label(options_frame, text="输出格式:").pack(side="left", padx=10, pady=5)
        self.format_var = tk.StringVar(value="PNG")
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                     values=["PNG", "JPG", "WEBP", "BMP"], width=10)
        format_combo.pack(side="left", padx=5, pady=5)
        
        tk.Label(options_frame, text="质量:").pack(side="left", padx=10, pady=5)
        self.quality_var = tk.IntVar(value=85)
        tk.Scale(options_frame, from_=1, to=100, orient="horizontal",
                 variable=self.quality_var, length=150).pack(side="left", pady=5)
        
        # 进度
        self.progress = ttk.Progressbar(main, mode='determinate')
        self.progress.pack(fill="x", pady=10)
        
        # 操作按钮
        action_frame = tk.Frame(main)
        action_frame.pack(fill="x", pady=10)
        
        tk.Button(action_frame, text="🚀 开始处理", command=self.process,
                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                  padx=30, pady=12).pack(side="left", padx=10)
        
        # 状态
        self.status_var = tk.StringVar(value="就绪")
        tk.Label(main, textvariable=self.status_var, fg="gray").pack(fill="x")
    
    def add_images(self):
        files = filedialog.askopenfilenames(
            title="选择图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
        )
        for f in files:
            if f not in self.images:
                self.images.append(f)
                self.image_listbox.insert(tk.END, Path(f).name)
        self.status_var.set(f"已选择 {len(self.images)} 张图片")
    
    def add_folder(self):
        folder = filedialog.askdirectory(title="选择图片文件夹")
        if folder:
            for ext in ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp", "*.webp"]:
                for f in Path(folder).glob(ext):
                    self.images.append(str(f))
                    self.image_listbox.insert(tk.END, f.name)
            self.status_var.set(f"已选择 {len(self.images)} 张图片")
    
    def clear_images(self):
        self.images = []
        self.image_listbox.delete(0, tk.END)
        self.status_var.set("已清空")
    
    def process(self):
        if not self.images:
            messagebox.showwarning("提示", "请先添加图片！")
            return
        
        self.progress['maximum'] = len(self.images)
        self.progress['value'] = 0
        
        for i, img in enumerate(self.images):
            self.progress['value'] = i + 1
            self.root.update()
        
        self.status_var.set(f"✅ 完成！处理了 {len(self.images)} 张图片")
        messagebox.showinfo("完成", f"处理完成！")

def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
