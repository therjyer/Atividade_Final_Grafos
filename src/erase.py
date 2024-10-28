import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class EraseGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apagar Grafo")

        self.graph_data = {}
        self.load_graphs()

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.create_widgets()

    def load_graphs(self):
        if not os.path.exists("../lib/adjacency_matrix.json"):
            messagebox.showerror("Erro", "Arquivo adjacency_matrix.json não encontrado.")
            self.root.destroy()
            return

        with open("../lib/adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        
        self.graph_names = list(self.graph_data.keys())

    def create_widgets(self):
        tk.Label(self.scrollable_frame, text="Selecione um grafo para apagar:").pack(pady=10)

        for graph_name in self.graph_names:
            button = tk.Button(self.scrollable_frame, text=graph_name, command=lambda name=graph_name: self.confirm_delete(name))
            button.pack(pady=5, fill='x')

    def confirm_delete(self, graph_name):
        confirm = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja apagar o grafo '{graph_name}'?")
        if confirm:
            del self.graph_data[graph_name]
            self.save_changes()
            messagebox.showinfo("Apagado", f"Grafo '{graph_name}' foi apagado.")
            self.refresh_buttons()

    def save_changes(self):
        with open("../lib/adjacency_matrix.json", "w") as f:
            json.dump(self.graph_data, f, indent=4)

    def refresh_buttons(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_widgets()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = EraseGraphApp(root)
    root.mainloop()