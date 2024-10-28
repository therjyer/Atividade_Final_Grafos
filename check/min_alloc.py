import tkinter as tk 
from scipy.optimize import linear_sum_assignment
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
        
        self.log_text = tk.Text(self.root, height=20, width=70)
        self.log_text.pack()
        
        tk.Button(self.root, text="Encontrar Alocação Mínima", command=self.find_minimum_allocation).pack(pady=20)

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
        self.log_message("Convertendo a matriz de adjacência para não direcionada...")
        undirected_matrix = {}
        for u in adjacency_matrix:
            undirected_matrix[u] = {}
            for v, weight in adjacency_matrix[u].items():
                if weight > 0:
                    undirected_matrix[u][v] = weight
                    if v not in undirected_matrix:
                        undirected_matrix[v] = {}
                    undirected_matrix[v][u] = weight
        self.log_message("Conversão concluída.")
        return undirected_matrix

    def convert_to_bipartite(self, adjacency_matrix):
        self.log_message("Convertendo o grafo em um bipartido completo e ponderado...")
        vertices = list(adjacency_matrix.keys())
        mid_point = len(vertices) // 2

        bipartite_matrix = {f'left_{v}': {} for v in vertices[:mid_point]}
        bipartite_matrix.update({f'right_{v}': {} for v in vertices[mid_point:]})

        for u in bipartite_matrix.keys():
            for v in bipartite_matrix.keys():
                if u != v:
                    weight = adjacency_matrix.get(u.replace('left_', ''), {}).get(v.replace('right_', ''), 1)
                    bipartite_matrix[u][v] = weight

        self.log_message("Conversão concluída.")
        return bipartite_matrix

    def find_minimum_allocation(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Iniciando a busca pela alocação mínima...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        if not graph_info.get('has_weights', False):
            self.log_message("Transformando em bipartido completo e ponderado.")
            adjacency_matrix = self.convert_to_bipartite(graph_info['adjacency_matrix'])
        else:
            adjacency_matrix = self.make_undirected(graph_info['adjacency_matrix'])

        cost_matrix = []
        vertices = list(adjacency_matrix.keys())
        self.log_message("Construindo a matriz de custo...")

        for u in vertices:
            cost_row = [adjacency_matrix[u].get(v, float('inf')) for v in vertices]
            cost_matrix.append(cost_row)
            self.log_message(f"Matriz de custo para {u}: {cost_row}")

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        min_cost = sum(cost_matrix[row][col] for row, col in zip(row_ind, col_ind))

        allocation = [f"{vertices[row]} -> {vertices[col]}" for row, col in zip(row_ind, col_ind)]
        self.log_message(f"Alocação mínima com custo {min_cost}:")
        self.log_message("\n".join(allocation))
        messagebox.showinfo("Alocação Mínima", f"Alocação mínima com custo {min_cost}:\n" + "\n".join(allocation))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = VerificationApp(root)
    root.mainloop()