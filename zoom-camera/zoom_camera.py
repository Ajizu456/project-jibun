import cv2
import tkinter as tk
from tkinter import Label, messagebox, StringVar, OptionMenu
from PIL import Image, ImageTk
import time

# Dictionary untuk terjemahan tombol
LANGUAGES = {
    "English": {
        "screenshot": "Screenshot", "fullscreen": "Fullscreen",
        "screenshot_msg": "Screenshot saved as screenshot.png"
    },
    "日本語": {
        "screenshot": "スクリーンショット", "fullscreen": "フルスクリーン",
        "screenshot_msg": "スクリーンショットが保存されました"
    },
    "Bahasa Indonesia": {
        "screenshot": "Tangkap Layar", "fullscreen": "Layar Penuh",
        "screenshot_msg": "Screenshot berhasil disimpan"
    }
}

class KacaPembesarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kaca Pembesar Digital")
        
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            retry = messagebox.askretrycancel("Error", "Kamera tidak dapat dibuka! Coba lagi?")
            if retry:
                self.cap = cv2.VideoCapture(0)
            else:
                self.root.destroy()
        
        self.zoom_factor = 1.0
        
        # Pilihan bahasa
        self.selected_lang = StringVar(value="English")
        self.lang_menu = OptionMenu(root, self.selected_lang, *LANGUAGES.keys())
        self.lang_menu.pack(pady=5)
        
        # Label video
        self.label = Label(root)
        self.label.pack(fill="both", expand=True)
        
        # Label zoom
        self.zoom_label = Label(root, text=f"Zoom: {self.zoom_factor:.1f}x", font=("Arial", 12, "bold"))
        self.zoom_label.pack()
        
        # Label FPS
        self.fps_label = Label(root, text="FPS: 0", font=("Arial", 12, "bold"))
        self.fps_label.pack()
        self.last_time = time.time()
        
        # Fullscreen mode
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)
        
        # Resize window dynamically
        self.root.bind("<Configure>", self.resize_window)
        
        # Mouse wheel zoom
        self.bind_mouse_wheel()
        
        # Keyboard shortcuts
        self.root.bind("<Control-plus>", lambda event: self.zoom_in())
        self.root.bind("<Control-minus>", lambda event: self.zoom_out())
        self.root.bind("<Control-s>", lambda event: self.screenshot())
        
        self.update_frame()
    
    def bind_mouse_wheel(self):
        self.root.bind("<MouseWheel>", self.mouse_zoom)
        self.root.bind("<Button-4>", self.mouse_zoom)
        self.root.bind("<Button-5>", self.mouse_zoom)

    def mouse_zoom(self, event):
        if event.delta > 0 or event.num == 4:
            self.zoom_in()
        elif event.delta < 0 or event.num == 5:
            self.zoom_out()
    
    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            height, width = frame.shape[:2]
            center_x, center_y = width // 2, height // 2
            radius_x, radius_y = min(center_x, int(width // (2 * self.zoom_factor))), min(center_y, int(height // (2 * self.zoom_factor)))
            cropped_frame = frame[center_y - radius_y:center_y + radius_y, center_x - radius_x:center_x + radius_x]
            zoomed_frame = cv2.resize(cropped_frame, (width, height), interpolation=cv2.INTER_LINEAR)
            
            img = cv2.cvtColor(zoomed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
            
            # Update FPS
            current_time = time.time()
            fps = 1 / (current_time - self.last_time)
            self.last_time = current_time
            self.fps_label.config(text=f"FPS: {fps:.2f}")
        
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
    
    def resize_window(self, event):
        self.label.config(width=event.width, height=event.height)
    
    def exit_program(self):
        self.cap.release()
        self.root.destroy()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = KacaPembesarApp(root)
    root.mainloop()
