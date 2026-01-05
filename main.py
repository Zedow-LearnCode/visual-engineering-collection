import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import importlib
import sys
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

PLUGINS_DIR = "plugins"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Python Visualizer")

        self.after(0, lambda: self.state("zoomed"))

        self.current_plugin = None
        self.plugin_instance = None
        self.is_focus_mode = False

        self._setup_ui()
        self.refresh_plugins()

        self.bind("<Escape>", lambda e: self.toggle_focus_mode())

    def _setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar, text="DEMO LIST", font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        ctk.CTkButton(
            self.sidebar,
            text="[ ] Focus Mode",
            command=self.toggle_focus_mode,
            fg_color="#444",
            hover_color="#666",
            border_width=1,
            border_color="#888",
        ).pack(padx=20, pady=(0, 20))

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.sidebar, label_text="Select Effect"
        )
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(
            self.sidebar,
            text="Reload Code",
            command=self.reload_plugin,
            fg_color="#2CC985",
            hover_color="#229964",
        ).pack(padx=20, pady=20)

        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.container = tk.Frame(self.right_panel, bg="#1e1e1e")
        self.container.pack(fill="both", expand=True)

    def toggle_focus_mode(self):
        if not self.is_focus_mode:

            self.sidebar.grid_forget()

            self.right_panel.grid(
                row=0, column=0, columnspan=2, sticky="nsew", padx=0, pady=0
            )
            self.is_focus_mode = True
        else:

            self.sidebar.grid(row=0, column=0, sticky="nsew")

            self.right_panel.grid(
                row=0, column=1, columnspan=1, sticky="nsew", padx=20, pady=20
            )
            self.is_focus_mode = False

    def refresh_plugins(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not os.path.isdir(PLUGINS_DIR):
            os.makedirs(PLUGINS_DIR)

        files = [
            f[:-3]
            for f in os.listdir(PLUGINS_DIR)
            if f.endswith(".py") and f != "__init__.py"
        ]

        for f in sorted(files):
            btn = ctk.CTkButton(
                self.scroll_frame,
                text=f"Run: {f}",
                command=lambda name=f: self.load_plugin(name),
                fg_color="transparent",
                border_width=1,
                text_color=("gray10", "#DCE4EE"),
            )
            btn.pack(pady=2, fill="x")

    def unload_current(self):
        if self.plugin_instance and hasattr(self.plugin_instance, "teardown"):
            try:
                self.plugin_instance.teardown()
            except:
                pass

        for widget in self.container.winfo_children():
            widget.destroy()

        self.plugin_instance = None

    def load_plugin(self, plugin_name=None):
        if not plugin_name:
            if not hasattr(self, "last_loaded_name"):
                return
            plugin_name = self.last_loaded_name

        self.last_loaded_name = plugin_name
        module_name = f"{PLUGINS_DIR}.{plugin_name}"

        self.unload_current()

        try:
            if module_name in sys.modules:
                module = importlib.reload(sys.modules[module_name])
            else:
                module = importlib.import_module(module_name)

            if hasattr(module, "Plugin"):
                self.plugin_instance = module.Plugin(self.container)
                self.plugin_instance.pack(fill="both", expand=True)
            else:
                messagebox.showerror("Error", "Class 'Plugin' not found")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reload_plugin(self):
        self.load_plugin()


if __name__ == "__main__":
    app = App()
    app.mainloop()
