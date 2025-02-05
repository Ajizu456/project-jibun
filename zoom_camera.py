import cv2
import tkinter as tk
from tkinter import Label, Button, messagebox, StringVar, OptionMenu
from PIL import Image, ImageTk
import time

# Dictionary untuk terjemahan tombol
LANGUAGES = {
    "English": {
        "zoom_in": "Zoom In", "zoom_out": "Zoom Out", "screenshot": "Screenshot", "exit": "Exit", "fullscreen": "Fullscreen",
        "screenshot_msg": "Screenshot saved as screenshot.png"
    },
    "日本語": {
        "zoom_in": "ズームイン", "zoom_out": "ズームアウト", "screenshot": "スクリーンショット", "exit": "終了", "fullscreen": "フルスクリーン",
        "screenshot_msg": "スクリーンショットが 'screenshot.png' に保存されました"
    },
    "Bahasa Indonesia": {
        "zoom_in": "Perbesar", "zoom_out": "Perkecil", "screenshot": "Tangkap Layar", "exit": "Keluar", "fullscreen": "Layar Penuh",
        "screenshot_msg": "Screenshot berhasil disimpan sebagai screenshot.png"
    }
}


class KacaPembesarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("デジタル拡大鏡")

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Kamera tidak dapat dibuka!")
            exit()

        self.zoom_factor = 1.0

        # Pilihan bahasa
        self.selected_lang = StringVar(value="English")
        self.lang_menu = OptionMenu(root, self.selected_lang, *LANGUAGES.keys(), command=self.update_language)
        self.lang_menu.pack(pady=5)

        # Label untuk menampilkan video
        self.label = Label(root)
        self.label.pack(fill="both", expand=True)

         
        # Label zoom
        self.zoom_label = Label(root, text=f"Zoom: {self.zoom_factor:.1f}x", font=("Arial", 12, "bold"))
        self.zoom_label.pack()


        # Fullscreen mode dengan tombol F11 & ESC
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Tambahkan event listener untuk scroll zoom
        self.bind_mouse_wheel()
         
        # Keyboard shortcuts
        self.root.bind("<Control-plus>", lambda event: self.zoom_in())
        self.root.bind("<Control-minus>", lambda event: self.zoom_out())
        self.root.bind("<Control-s>", lambda event: self.screenshot())

        # Perbarui teks tombol sesuai bahasa awal
        self.update_language("English")

        self.update_frame()

    def update_language(self, lang):
        pass

    def bind_mouse_wheel(self):
        self.root.bind("<MouseWheel>", self.mouse_zoom)  # Windows/Mac
        self.root.bind("<Button-4>", self.mouse_zoom)  # Linux (scroll up)
        self.root.bind("<Button-5>", self.mouse_zoom)  # Linux (scroll down)

    def mouse_zoom(self, event):
        if event.delta > 0 or event.num == 4:  # Scroll ke atas (zoom in)
            self.zoom_in()
        elif event.delta < 0 or event.num == 5:  # Scroll ke bawah (zoom out)
            self.zoom_out()

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            height, width = frame.shape[:2]
            center_x, center_y = width // 2, height // 2
            radius_x, radius_y = int(width // (2 * self.zoom_factor)), int(height // (2 * self.zoom_factor))
            cropped_frame = frame[center_y - radius_y:center_y + radius_y, center_x - radius_x:center_x + radius_x]
            zoomed_frame = cv2.resize(cropped_frame, (width, height), interpolation=cv2.INTER_LINEAR)

            img = cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.root.after(10, self.update_frame)

    def zoom_in(self):
        if self.zoom_factor < 2.0:
            self.zoom_factor += 0.1
            self.zoom_label.config(text=f"Zoom: {self.zoom_factor:.1f}x")

    def zoom_out(self):
        if self.zoom_factor > 1.0:
            self.zoom_factor -= 0.1
            self.zoom_label.config(text=f"Zoom: {self.zoom_factor:.1f}x")

    
    def screenshot(self):
        ret, frame = self.cap.read()
        if ret:
            height, width = frame.shape[:2]
            center_x, center_y = width // 2, height // 2
            radius_x, radius_y = int(width // (2 * self.zoom_factor)), int(height // (2 * self.zoom_factor))
            cropped_frame = frame[center_y - radius_y:center_y + radius_y, center_x - radius_x:center_x + radius_x]
            zoomed_frame = cv2.resize(cropped_frame, (width, height), interpolation=cv2.INTER_LINEAR)
            filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(filename, zoomed_frame)
            lang = self.selected_lang.get()
            messagebox.showinfo("Screenshot", f"{LANGUAGES[lang]['screenshot_msg']}: {filename}")

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.root.attributes("-fullscreen", False)

    def exit_program(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = KacaPembesarApp(root)
    root.mainloop()
