import tkinter as tk
from tkinter import messagebox
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
        
        tk.Button(self.root, text="Verificar se o Grafo é Não Direcionado e Conectado", command=self.check_if_undirected_and_connected).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_if_undirected_and_connected(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Iniciando a verificação se o grafo é não direcionado e conectado...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        def is_undirected():
            self.log_message("Verificando se o grafo é não direcionado...")
            for u in adjacency_matrix:
                for v in adjacency_matrix[u]:
                    if adjacency_matrix[u][v] != adjacency_matrix[v].get(u, 0):
                        self.log_message(f"Grafo é direcionado: {u} -> {v} diferente de {v} -> {u}.")
                        return False
            self.log_message("O grafo é não direcionado.")
            return True

        def is_connected():
            self.log_message("Verificando se o grafo está conectado...")
            visited = set()

            def dfs(v):
                visited.add(v)
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                        dfs(neighbor)

            initial_vertex = next(iter(adjacency_matrix))
            dfs(initial_vertex)

            if len(visited) == len(adjacency_matrix):
                self.log_message("O grafo está conectado.")
                return True
            else:
                self.log_message("O grafo não está conectado.")
                return False

        if is_undirected():
            if is_connected():
                messagebox.showinfo("Verificação do Grafo", "O grafo é não direcionado e conectado.")
            else:
                messagebox.showinfo("Verificação do Grafo", "O grafo é não direcionado, mas não está conectado.")
        else:
            messagebox.showinfo("Verificação do Grafo", "O grafo é direcionado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()