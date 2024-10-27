import tkinter as tk 
from tkinter import messagebox
import json
import os
from itertools import combinations

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
        
        tk.Button(self.root, text="Verificar Planaridade", command=self.check_planarity).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_planarity(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Iniciando a verificação de planaridade...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        vertices = list(adjacency_matrix.keys())
        v = len(vertices)
        e = sum(len([n for n in adjacency_matrix[vertex] if adjacency_matrix[vertex][n] != 0]) for vertex in vertices) // 2

        self.log_message(f"Número de vértices: {v}, Número de arestas: {e}")

        if e > 3 * v - 6:
            self.log_message("O grafo não é planar pela fórmula de Euler.")
            messagebox.showinfo("Verificação de Planaridade", "O grafo não é planar pela fórmula de Euler.")
            return

        def contains_k5_k33(graph):
            self.log_message("Verificando se o grafo contém subgrafos homeomorfos a K5 ou K3,3...")
            for comb in combinations(graph.keys(), 5):
                subgraph = {v: set(n for n in graph[v] if n in comb) for v in comb}
                if all(len(neighbors) == 4 for neighbors in subgraph.values()):
                    self.log_message("O grafo contém um subgrafo homeomorfo a K5.")
                    return True

            for comb in combinations(graph.keys(), 6):
                set1, set2 = comb[:3], comb[3:]
                is_k33 = all(adjacency_matrix[v1][v2] != 0 for v1 in set1 for v2 in set2) and \
                          all(adjacency_matrix[v1][v2] == 0 for v1 in set1 for v2 in set1) and \
                          all(adjacency_matrix[v1][v2] == 0 for v1 in set2 for v2 in set2)
                if is_k33:
                    self.log_message("O grafo contém um subgrafo homeomorfo a K3,3.")
                    return True

            self.log_message("Nenhum subgrafo proibido encontrado.")
            return False

        if contains_k5_k33(adjacency_matrix):
            self.log_message("O grafo não é planar devido a subgrafos proibidos.")
            messagebox.showinfo("Verificação de Planaridade", "O grafo contém um subgrafo homeomorfo a K5 ou K3,3, então não é planar.")
        else:
            self.log_message("O grafo é planar.")
            messagebox.showinfo("Verificação de Planaridade", "O grafo é planar.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()
