import tkinter as tk
import struct
from tkinter import colorchooser, messagebox, filedialog
# AurumPallette v9.0 Sketchboard
# Copyright (C) 2026 (Mr.Cobalt)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.
class AurumPallette:
    def __init__(self, root):
        self.root = root
        self.root.title("AurumPallette v9.0 Sketchboard")
        self.root.geometry("1100x750")
        self.root.configure(bg="#2c3e50")

        self.current_line = []
        self.color_rgb = (0, 0, 0)
        self.hex_color = "#000000"
        self.brush_size = 2
        self.current_file = "autosave.aup"
        self.eraser_mode = False

        self.controls = tk.Frame(self.root, width=200, bg="#34495e", padx=10, pady=10)
        self.controls.pack(side="left", fill="y")

        tk.Label(self.controls, text="AurumPallette", fg="#f1c40f", bg="#34495e", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.controls, text="Choose Color", command=self.renk_sec, width=18, bg="#ecf0f1").pack(pady=5)
        
        self.btn_eraser = tk.Button(self.controls, text="Rubber: OFF", command=self.toggle_eraser, width=18, bg="#95a5a6", fg="white")
        self.btn_eraser.pack(pady=5)

        tk.Button(self.controls, text="Read file (.aup)", command=self.aup_yukle, width=18, bg="#27ae60", fg="white").pack(pady=5)
        tk.Button(self.controls, text="Save as...", command=self.farkli_kaydet, width=18, bg="#3498db", fg="white").pack(pady=5)
        tk.Button(self.controls, text="Clean the canvas", command=self.ekrani_temizle, width=18, bg="#e74c3c", fg="white").pack(pady=20)

        tk.Label(self.controls, text="Brush / Rubber Thickness:", fg="white", bg="#34495e").pack()
        self.size_slider = tk.Scale(self.controls, from_=1, to=50, orient="horizontal", bg="#34495e", fg="white", highlightthickness=0)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(pady=5, fill="x")

        tk.Label(self.controls, text="Selected color:", fg="white", bg="#34495e").pack(pady=(20, 0))
        self.color_display = tk.Label(self.controls, bg="black", width=12, height=2, relief="sunken")
        self.color_display.pack(pady=5)

        self.canvas = tk.Canvas(self.root, bg="white", cursor="pencil", bd=0, highlightthickness=0)
        self.canvas.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        self.canvas.bind("<B1-Motion>", self.ciz)
        self.canvas.bind("<ButtonRelease-1>", self.otomatik_kaydet)

    def toggle_eraser(self):
        self.eraser_mode = not self.eraser_mode
        if self.eraser_mode:
            self.btn_eraser.config(text="Rubber: ON", bg="#e67e22")
            self.canvas.config(cursor="dot")
        else:
            self.btn_eraser.config(text="Rubber: OFF", bg="#95a5a6")
            self.canvas.config(cursor="pencil")

    def renk_sec(self):
        self.eraser_mode = False 
        self.btn_eraser.config(text="Rubber: OFF", bg="#95a5a6")
        color = colorchooser.askcolor(title="Choose color")
        if color[1]:
            self.hex_color = color[1]
            self.color_rgb = tuple(map(int, color[0]))
            self.color_display.config(bg=self.hex_color)

    def ekrani_temizle(self):
        if messagebox.askyesno("Confirmation", "Are you sure you want to reset the canvas?"):
            self.canvas.delete("all")
            with open(self.current_file, "wb") as f:
                pass

    def farkli_kaydet(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".aup", filetypes=[("AurumPallette Sketch", "*.aup")])
        if file_path:
            self.current_file = file_path
            self.root.title(f"Aurum Pallette - {self.current_file}")

    def ciz(self, event):
        size = self.size_slider.get()
        draw_color = "white" if self.eraser_mode else self.hex_color
        
        x1, y1 = (event.x - size), (event.y - size)
        x2, y2 = (event.x + size), (event.y + size)
        
        self.canvas.create_oval(x1, y1, x2, y2, fill=draw_color, outline=draw_color)
        self.current_line.append((event.x, event.y, size, draw_color))

    def otomatik_kaydet(self, event):
        if not self.current_line: return
        with open(self.current_file, "ab") as f:
            for x, y, size, color in self.current_line:
                if color == "white":
                    r, g, b = (255, 255, 255)
                else:
                    r, g, b = self.color_rgb
                
                f.write(struct.pack('BBBB', r, g, b, size))
                f.write(struct.pack('ii', x, y))
                f.write(struct.pack('ii', -1, -1)) 
        self.current_line = []

    def aup_yukle(self):
        file_path = filedialog.askopenfilename(filetypes=[("AurumPallette", "*.aup")])
        if not file_path: return
        try:
            with open(file_path, "rb") as f:
                self.canvas.delete("all")
                self.current_file = file_path
                while True:
                    header = f.read(4)
                    if not header or len(header) < 4: break
                    r, g, b, size = struct.unpack('BBBB', header)
                    current_hex = '#%02x%02x%02x' % (r, g, b)
                    
                    coord_data = f.read(8)
                    if not coord_data: break
                    x, y = struct.unpack('ii', coord_data)
                    
                    f.read(8) 
                    
                    x1, y1 = (x - size), (y - size)
                    x2, y2 = (x + size), (y + size)
                    self.canvas.create_oval(x1, y1, x2, y2, fill=current_hex, outline=current_hex)
            self.root.title(f"Aurum Pallette - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"File couldn't read': {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AurumPallette(root)
    root.mainloop()