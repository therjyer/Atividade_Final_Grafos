import tkinter as tk
from tkinter import messagebox
import json
import os

class VerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificações de Gráficos")
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
        tk.Label(self.root, text="Selecione um gráfico para verificação:").pack()
        self.selected_graph = tk.StringVar(value="Escolha um gráfico")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()
        
        self.log_text = tk.Text(self.root, height=15, width=50)
        self.log_text.pack()
        
        tk.Button(self.root, text="Encontrar Alocação Mínima (Hungarian)", command=self.find_minimum_allocation).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um gráfico" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de gráfico válido.")
            return None
        return self.graph_data[graph_name]

    def make_undirected(self, adjacency_matrix):
        undirected_matrix = {}
        for u in adjacency_matrix:
            undirected_matrix[u] = {}
            for v, weight in adjacency_matrix[u].items():
                if weight > 0:
                    undirected_matrix[u][v] = weight
                    if v not in undirected_matrix:
                        undirected_matrix[v] = {}
                    undirected_matrix[v][u] = weight
        return undirected_matrix

    def find_minimum_allocation(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        if not graph_info.get('has_weights', False):
            messagebox.showerror("Erro", "A alocação mínima só se aplica a gráficos bipartidos completos e ponderados.")
            return

        adjacency_matrix = self.make_undirected(graph_info['adjacency_matrix'])

        cost_matrix = []
        vertices = list(adjacency_matrix.keys())
        for u in vertices:
            cost_row = [adjacency_matrix[u].get(v, float('inf')) for v in vertices]
            cost_matrix.append(cost_row)

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        min_cost = sum(cost_matrix[row][col] for row, col in zip(row_ind, col_ind))

        allocation = [f"{vertices[row]} -> {vertices[col]}" for row, col in zip(row_ind, col_ind)]
        self.log_message(f"Alocação mínima com custo {min_cost}:")
        self.log_message("\n".join(allocation))
        messagebox.showinfo("Alocação Mínima", f"Alocação mínima com custo {min_cost}:\n" + "\n".join(allocation))
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()
