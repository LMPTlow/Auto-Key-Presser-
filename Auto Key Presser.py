import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import keyboard
import time
from threading import Thread, Event

class AutoPressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto KeyPresser   --Made by LMPT--")
        self.root.geometry("400x250")
        
        # Настройки по умолчанию
        self.is_running = False
        self.thread_event = Event()
        self.thread = None
        self.press_duration = 1.0
        self.release_duration = 0.1
        self.toggle_hotkey = "F5"
        self.target_key = "e"
        self.language = "ru"  # По умолчанию русский язык
        
        # Тексты для разных языков
        self.texts = {
            "ru": {
                "title": "Auto KeyPresser   --Made by LMPT--",
                "status_stopped": "Статус: Остановлено",
                "status_running": "Статус: Работает ({})",
                "target_key": "Автоматизируемая клавиша:",
                "press_duration": "Нажатие (сек):",
                "release_duration": "Отпускание (сек):",
                "hotkey": "Горячая клавиша:",
                "start": "Старт",
                "stop": "Стоп",
                "exit": "Выход",
                "change_key_title": "Изменить клавишу",
                "change_key_prompt": "Введите клавишу для автоматизации (например: e, f, space):",
                "change_hotkey_title": "Изменить горячую клавишу",
                "change_hotkey_prompt": "Введите новую клавишу для переключения (например: F5, F12):",
                "error": "Ошибка",
                "single_char": "Введите только один символ",
                "made_by": "Made by LMPT",
                "license": "License AEL© - Atlas Entertainment License 1.0.0"
            },
            "en": {
                "title": "Auto KeyPresser   --Made by LMPT--",
                "status_stopped": "Status: Stopped",
                "status_running": "Status: Running ({})",
                "target_key": "Target key:",
                "press_duration": "Press duration (sec):",
                "release_duration": "Release duration (sec):",
                "hotkey": "Hotkey:",
                "start": "Start",
                "stop": "Stop",
                "exit": "Exit",
                "change_key_title": "Change key",
                "change_key_prompt": "Enter key to automate (e.g.: e, f, space):",
                "change_hotkey_title": "Change hotkey",
                "change_hotkey_prompt": "Enter new toggle hotkey (e.g.: F5, F12):",
                "error": "Error",
                "single_char": "Please enter a single character",
                "made_by": "Made by LMPT",
                "license": "License AEL© - Atlas Entertainment License 1.0.0"
            }
        }
        
        self.create_widgets()
        self.setup_hotkeys()
    
    def create_widgets(self):
        # Language switch button (top-left)
        self.lang_button = ttk.Button(self.root, text="EN", width=3, 
                                     command=self.toggle_language)
        self.lang_button.place(x=10, y=10)
        
        # Status label
        self.status_label = ttk.Label(self.root, text=self.texts[self.language]["status_stopped"], 
                                    font=('Arial', 12))
        self.status_label.pack(pady=5)
        
        # Target key control
        target_frame = ttk.Frame(self.root)
        target_frame.pack(pady=5)
        
        ttk.Label(target_frame, text=self.texts[self.language]["target_key"]).grid(row=0, column=0)
        self.target_key_btn = ttk.Button(target_frame, text=self.target_key.upper(), 
                                       width=3, command=self.change_target_key)
        self.target_key_btn.grid(row=0, column=1, padx=5)
        
        # Duration controls
        duration_frame = ttk.Frame(self.root)
        duration_frame.pack(pady=5)
        
        ttk.Label(duration_frame, text=self.texts[self.language]["press_duration"]).grid(row=0, column=0)
        self.press_entry = ttk.Entry(duration_frame, width=5)
        self.press_entry.insert(0, str(self.press_duration))
        self.press_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(duration_frame, text=self.texts[self.language]["release_duration"]).grid(row=1, column=0)
        self.release_entry = ttk.Entry(duration_frame, width=5)
        self.release_entry.insert(0, str(self.release_duration))
        self.release_entry.grid(row=1, column=1, padx=5)
        
        # Hotkey control
        hotkey_frame = ttk.Frame(self.root)
        hotkey_frame.pack(pady=5)
        
        ttk.Label(hotkey_frame, text=self.texts[self.language]["hotkey"]).grid(row=0, column=0)
        self.hotkey_btn = ttk.Button(hotkey_frame, text=self.toggle_hotkey.upper(), 
                                   command=self.change_toggle_hotkey)
        self.hotkey_btn.grid(row=0, column=1, padx=5)
        
        # Control buttons
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.toggle_button = ttk.Button(control_frame, text=self.texts[self.language]["start"], 
                                      command=self.toggle_pressing)
        self.toggle_button.grid(row=0, column=0, padx=5)
        
        self.exit_button = ttk.Button(control_frame, text=self.texts[self.language]["exit"], 
                                    command=self.root.quit)
        self.exit_button.grid(row=0, column=1, padx=5)
        
        # Signature (добавлено в правый нижний угол)
        self.signature = ttk.Label(self.root, text=self.texts[self.language]["made_by"], 
                                  font=('Arial', 8))
        self.signature.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-25)

        # License (добавлено в правый нижний угол)
        self.license = ttk.Label(self.root, text=self.texts[self.language]["license"], 
                                font=('Arial', 8))
        self.license.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-7)
    
    def toggle_language(self):
        """Переключение между русским и английским языком"""
        self.language = "en" if self.language == "ru" else "ru"
        self.lang_button.config(text="RU" if self.language == "en" else "EN")
        self.update_ui_text()
    
    def update_ui_text(self):
        """Обновление всех текстовых элементов интерфейса"""
        texts = self.texts[self.language]
        
        self.root.title(texts["title"])
        self.status_label.config(
            text=texts["status_running"].format(self.target_key.upper()) 
            if self.is_running else texts["status_stopped"]
        )
        
        # Обновляем все текстовые элементы
        for frame in self.root.winfo_children():
            if isinstance(frame, ttk.Frame):
                for widget in frame.winfo_children():
                    if isinstance(widget, ttk.Label):
                        if widget["text"] == self.texts["ru"]["target_key"] or widget["text"] == self.texts["en"]["target_key"]:
                            widget.config(text=texts["target_key"])
                        elif widget["text"] == self.texts["ru"]["press_duration"] or widget["text"] == self.texts["en"]["press_duration"]:
                            widget.config(text=texts["press_duration"])
                        elif widget["text"] == self.texts["ru"]["release_duration"] or widget["text"] == self.texts["en"]["release_duration"]:
                            widget.config(text=texts["release_duration"])
                        elif widget["text"] == self.texts["ru"]["hotkey"] or widget["text"] == self.texts["en"]["hotkey"]:
                            widget.config(text=texts["hotkey"])
        
        self.toggle_button.config(text=texts["stop"] if self.is_running else texts["start"])
        self.exit_button.config(text=texts["exit"])
        self.signature.config(text=texts["made_by"])
        self.license.config(text=texts["license"])
    
    def setup_hotkeys(self):
        keyboard.add_hotkey(self.toggle_hotkey, self.toggle_pressing)
    
    def change_target_key(self):
        new_key = simpledialog.askstring(
            self.texts[self.language]["change_key_title"],
            self.texts[self.language]["change_key_prompt"],
            parent=self.root
        )
        if new_key and len(new_key) == 1:
            self.target_key = new_key.lower()
            self.target_key_btn.config(text=self.target_key.upper())
            if self.is_running:
                self.status_label.config(
                    text=self.texts[self.language]["status_running"].format(self.target_key.upper())
                )
        elif new_key:
            messagebox.showerror(
                self.texts[self.language]["error"],
                self.texts[self.language]["single_char"]
            )
    
    def change_toggle_hotkey(self):
        new_hotkey = simpledialog.askstring(
            self.texts[self.language]["change_hotkey_title"],
            self.texts[self.language]["change_hotkey_prompt"],
            parent=self.root
        )
        if new_hotkey:
            keyboard.remove_hotkey(self.toggle_hotkey)
            self.toggle_hotkey = new_hotkey
            keyboard.add_hotkey(self.toggle_hotkey, self.toggle_pressing)
            self.hotkey_btn.config(text=self.toggle_hotkey.upper())
    
    def press_key_loop(self):
        self.press_duration = float(self.press_entry.get())
        self.release_duration = float(self.release_entry.get())
        
        while not self.thread_event.is_set():
            keyboard.press(self.target_key)
            time.sleep(self.press_duration)
            keyboard.release(self.target_key)
            time.sleep(self.release_duration)
    
    def toggle_pressing(self):
        if not self.is_running:
            # Start pressing
            self.is_running = True
            self.thread_event.clear()
            self.thread = Thread(target=self.press_key_loop)
            self.thread.start()
            
            self.status_label.config(
                text=self.texts[self.language]["status_running"].format(self.target_key.upper())
            )
            self.toggle_button.config(text=self.texts[self.language]["stop"])
        else:
            # Stop pressing
            self.is_running = False
            self.thread_event.set()
            if self.thread:
                self.thread.join()
            
            self.status_label.config(text=self.texts[self.language]["status_stopped"])
            self.toggle_button.config(text=self.texts[self.language]["start"])
    
    def on_closing(self):
        self.is_running = False
        self.thread_event.set()
        if self.thread:
            self.thread.join()
        keyboard.unhook_all()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoPressApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()