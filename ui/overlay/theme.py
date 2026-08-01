import tkinter as tk
from tkinter import ttk

BG = "#1E1E1E"
FG_MAIN = "#FFFFFF"
FG_HEADER = "#FFBB00"
FG_SECTION = "#64C4FF"
FG_VALUE = "#52E252"

def setup_overlay_style():
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TFrame", background=BG)
    style.configure("TLabel", background=BG, foreground=FG_MAIN)
    style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground=FG_HEADER)
    style.configure("Section.TLabel", font=("Segoe UI", 10, "bold"), foreground=FG_SECTION, padding=(0, 10, 0, 5))
    style.configure("Param.TLabel", font=("Segoe UI", 9))
    style.configure("Value.TLabel", font=("Segoe UI", 9, "bold"), foreground=FG_VALUE)
    return style

def setup_window_properties(root, title, geometry):
    root.title(title)
    root.attributes("-topmost", True)
    root.attributes("-alpha", 0.90)
    root.configure(bg=BG)
    root.geometry(geometry)
