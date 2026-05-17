#!/usr/bin/env python3
"""
图片压缩工具 - 真实功能
支持批量压缩 PNG/JPG/JPEG/WEBP
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
import tkinter as tk

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

class App:
    def __init__(self, root):
        self.root = root
        root.title("图片压缩工具 v1.0")
        root.geometry("650x500")
        self.files = []
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#1f538d", height=60)
        f.pack(fill="x")
        tk.Label(f, text="🖼️ 图片压缩工具", font=("Arial",16,"bold"),
                 fg="white", bg="#1f538d").pack(pady=15)
        main = tk.Frame(self.root, padx=20, pady=15)
        main.pack(fill="both", expand=True)
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="添加图片", command=self.add_files,
                  bg="#1f538d", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="清空列表", command=self.clear,
                  bg="#d9534f", fg="white", padx=15).pack(side="left", padx=5)
        tk.Button(bf, text="开始压缩", command=self.compress,
                  bg="#5cb85c", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(side="right", padx=5)
        # 质量滑动条
        sf = tk.Frame(main)
        sf.pack(fill="x", pady=5)
        tk.Label(sf, text="压缩质量：").pack(side="left")
        self.quality = tk.Scale(sf, from_=10, to=95, orient="horizontal", length=200)
        self.quality.set(70)
        self.quality.pack(side="left", padx=10)
        tk.Label(sf, text="（数值越小文件越小）").pack(side="left")
        self.lb = tk.Listbox(main, font=("Consolas",10), bg="#f8f9fa", height=12)
        self.lb.pack(fill="both", expand=True, pady=10)
        self.status = tk.Label(main, text="请添加图片（支持 JPG/PNG/WEBP）",
                              font=("Arial",10), fg="gray", anchor="w")
        self.status.pack(fill="x")
    
    def add_files(self):
        fs = filedialog.askopenfilenames(title="选择图片",
             filetypes=[("图片","*.jpg *.jpeg *.png *.webp *.bmp")])
        for f in fs:
            if f not in self.files:
                self.files.append(f)
                size = Path(f).stat().st_size // 1024
                self.lb.insert("end", f"{Path(f).name}  ({size} KB)")
        self.status.config(text=f"已添加 {len(self.files)} 张图片")
    
    def clear(self):
        self.files.clear()
        self.lb.delete(0, "end")
        self.status.config(text="列表已清空")
    
    def compress(self):
        if not self.files:
            messagebox.showwarning("提示", "请先添加图片")
            return
        if not HAS_PIL:
            messagebox.showerror("缺少依赖", "请运行：pip install Pillow")
            return
        out_dir = filedialog.askdirectory(title="选择输出目录")
        if not out_dir: return
        q = self.quality.get()
        ok = 0
        for f in self.files:
            try:
                img = Image.open(f)
                out = str(Path(out_dir) / (Path(f).stem + "_compressed.jpg"))
                img.save(out, "JPEG", quality=q, optimize=True)
                ok += 1
            except Exception as e:
                print(f"压缩失败 {f}: {e}")
        messagebox.showinfo("完成", f"成功压缩 {ok}/{len(self.files)} 张图片！\n输出目录：{out_dir}")
        self.status.config(text=f"✅ 完成：{ok}张图片已压缩")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
