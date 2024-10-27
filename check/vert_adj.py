import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class VerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificações de Grafos")
        self.graph_data = {}
        self.graph_names = []
        self.load_graphs()
        self.create_widgets()

    def load_graphs(self):
        if not os.path.exists("../lib/adjacency_matrix.json"):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            self.root.destroy()
            return
        with open("../lib/adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        self.graph_names = list(self.graph_data.keys())

    def create_widgets(self):
        tk.Label(self.root, text="Selecione um grafo para verificação:").pack()
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()
        
        self.log_text = tk.Text(self.root, height=15, width=50)
        self.log_text.pack()
        
        tk.Button(self.root, text="Verificar Adjacência do Vértice", command=self.check_vertex_adjacency).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_vertex_adjacency(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        vertex = simpledialog.askstring("Vértice", "Digite o vértice para verificar a adjacência:")

        if vertex:
            adjacency_matrix = graph_info['adjacency_matrix']
            if vertex in adjacency_matrix:
                adjacent_vertices = [v for v in adjacency_matrix[vertex] if adjacency_matrix[vertex][v] != 0]
                if adjacent_vertices:
                    messagebox.showinfo("Adjacência do Vértice", f"Vértices adjacentes a {vertex}: {', '.join(adjacent_vertices)}.")
                else:
                    messagebox.showinfo("Adjacência do Vértice", f"O vértice {vertex} não possui vértices adjacentes.")
            else:
                messagebox.showerror("Erro", f"O vértice {vertex} não existe no grafo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()