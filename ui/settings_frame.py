import customtkinter as ctk
from utils.settings import Settings
import os
from tkinter import filedialog

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        
        self.settings = Settings()
        
        self.label = ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=20, weight="bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # Appearance
        self.appearance_frame = ctk.CTkFrame(self)
        self.appearance_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(self.appearance_frame, text="Appearance Mode:").grid(row=0, column=0, padx=20, pady=10)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.appearance_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=1, padx=20, pady=10)
        self.appearance_mode_optionemenu.set(self.settings.get("theme"))

        # Download Path
        self.path_frame = ctk.CTkFrame(self)
        self.path_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(self.path_frame, text="Download Folder:").grid(row=0, column=0, padx=20, pady=10)
        self.path_entry = ctk.CTkEntry(self.path_frame, width=300)
        self.path_entry.grid(row=0, column=1, padx=10, pady=10)
        self.path_entry.insert(0, self.settings.get("download_path"))
        
        self.browse_btn = ctk.CTkButton(self.path_frame, text="Browse", width=80, command=self.browse_path)
        self.browse_btn.grid(row=0, column=2, padx=10, pady=10)

        # Default Quality
        self.quality_frame = ctk.CTkFrame(self)
        self.quality_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        ctk.CTkLabel(self.quality_frame, text="Default Quality:").grid(row=0, column=0, padx=20, pady=10)
        self.quality_menu = ctk.CTkOptionMenu(self.quality_frame, values=["Best", "1080p", "720p", "480p", "Audio Only"],
                                             command=lambda v: self.settings.set("default_quality", v))
        self.quality_menu.grid(row=0, column=1, padx=20, pady=10)
        self.quality_menu.set(self.settings.get("default_quality"))

        # Save Button
        self.save_btn = ctk.CTkButton(self, text="Save All Settings", command=self.save_settings)
        self.save_btn.grid(row=4, column=0, padx=20, pady=20)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.settings.set("theme", new_appearance_mode)

    def browse_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.path_entry.delete(0, ctk.END)
            self.path_entry.insert(0, directory)

    def save_settings(self):
        self.settings.set("download_path", self.path_entry.get())
        self.settings.save()
        # Show some feedback
        self.save_btn.configure(text="Settings Saved!", fg_color="green")
        self.after(2000, lambda: self.save_btn.configure(text="Save All Settings", fg_color=ctk.ThemeManager.theme["CTkButton"]["fg_color"]))
