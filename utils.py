def clear_widgets(window):
    for widget in window.winfo_children():
        widget.destroy()