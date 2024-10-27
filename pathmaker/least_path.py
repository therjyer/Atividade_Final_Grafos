import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import deque
import json
import os

class VerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificações de grafos")
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
        
        tk.Button(self.root, text="Encontrar Caminho Mais Curto", command=self.find_shortest_path).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def find_shortest_path(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        start_vertex = simpledialog.askstring("Entrada", "Digite o vértice de início:")
        end_vertex = simpledialog.askstring("Entrada", "Digite o vértice de término:")

        if start_vertex not in adjacency_matrix or end_vertex not in adjacency_matrix:
            messagebox.showerror("Erro", "Um ou ambos os vértices não existem no grafo.")
            return

        path = self.bfs_shortest_path(adjacency_matrix, start_vertex, end_vertex)
        if path:
            self.log_message(f"Caminho mais curto de {start_vertex} para {end_vertex}: " + " -> ".join(path))
            messagebox.showinfo("Caminho Mais Curto", f"Caminho mais curto de {start_vertex} para {end_vertex}: " + " -> ".join(path))
        else:
            self.log_message(f"Não existe caminho entre {start_vertex} e {end_vertex}.")
            messagebox.showerror("Sem Caminho", f"Não existe caminho entre {start_vertex} e {end_vertex}.")

    def bfs_shortest_path(self, adjacency_matrix, start, goal):
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            vertex = path[-1]

            if vertex == goal:
                return path

            elif vertex not in visited:
                for neighbor in adjacency_matrix[vertex]:
                    if adjacency_matrix[vertex][neighbor] != 0:
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)

                visited.add(vertex)

        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()
