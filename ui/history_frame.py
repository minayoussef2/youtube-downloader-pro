import customtkinter as ctk
from core.stats_manager import StatsManager

class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.stats_manager = StatsManager()
        
        self.label = ctk.CTkLabel(self, text="Download History", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Recent Downloads")
        self.scrollable_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        
        self.refresh()

    def refresh(self):
        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        history = self.stats_manager.get_history()
        if not history:
            no_history = ctk.CTkLabel(self.scrollable_frame, text="No download history yet.")
            no_history.grid(row=0, column=0, pady=20)
            return
            
        for i, item in enumerate(history):
            item_frame = ctk.CTkFrame(self.scrollable_frame)
            item_frame.grid(row=i, column=0, padx=10, pady=5, sticky="ew")
            item_frame.grid_columnconfigure(1, weight=1)
            
            title = item.get('title', 'Unknown')
            timestamp = item.get('timestamp', '')
            quality = item.get('quality', '')
            
            title_label = ctk.CTkLabel(item_frame, text=title, font=ctk.CTkFont(weight="bold"), anchor="w")
            title_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")
            
            info_label = ctk.CTkLabel(item_frame, text=f"{timestamp} | {quality}", font=ctk.CTkFont(size=10), text_color="gray")
            info_label.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="w")
            
            open_btn = ctk.CTkButton(item_frame, text="Open Folder", width=100, height=24)
            open_btn.grid(row=0, column=1, rowspan=2, padx=10, sticky="e")
