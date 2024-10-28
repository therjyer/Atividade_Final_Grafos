import tkinter as tk
from tkinter import messagebox
import json
import os

class EraseGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apagar Grafo")

        self.graph_data = {}
        self.load_graphs()
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
        tk.Label(self.root, text="Selecione um grafo para apagar:").pack(pady=10)
        
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack(pady=10)

        tk.Button(self.root, text="Apagar Grafo", command=self.delete_graph).pack(pady=10)

    def delete_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um grafo válido para apagar.")
            return

        confirm = messagebox.askyesno("Confirmar Exclusão", f"Você tem certeza que deseja apagar o grafo '{graph_name}'?")
        if confirm:
            del self.graph_data[graph_name]
            self.save_changes()
            messagebox.showinfo("Apagado", f"Grafo '{graph_name}' foi apagado.")

    def save_changes(self):
        with open("../lib/adjacency_matrix.json", "w") as f:
            json.dump(self.graph_data, f, indent=4)
        messagebox.showinfo("Salvo", "Alterações salvas em adjacency_matrix.json")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = EraseGraphApp(root)
    root.mainloop()