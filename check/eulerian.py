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
        
        tk.Button(self.root, text="Verificar se o Grafo é Euleriano", command=self.check_eulerian).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_eulerian(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Iniciando a verificação do grafo Euleriano...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        def is_directed():
            for u in adjacency_matrix:
                for v in adjacency_matrix[u]:
                    if adjacency_matrix[u][v] != adjacency_matrix[v].get(u, 0):
                        return True
            return False

        def is_directed_eulerian():
            self.log_message("Verificando se todos os vértices têm grau de entrada e grau de saída iguais...")

            in_degree = {v: 0 for v in adjacency_matrix}
            out_degree = {v: 0 for v in adjacency_matrix}

            for u in adjacency_matrix:
                for v in adjacency_matrix[u]:
                    if adjacency_matrix[u][v] != 0:
                        out_degree[u] += 1
                        in_degree[v] += 1

            for v in adjacency_matrix:
                self.log_message(f"Vértice {v}: grau de entrada = {in_degree[v]}, grau de saída = {out_degree[v]}.")
                if in_degree[v] != out_degree[v]:
                    self.log_message(f"Vértice {v} não possui grau de entrada e saída iguais. O grafo não é Euleriano.")
                    return False

            def is_weakly_connected():
                visited = set()
                def dfs(v):
                    visited.add(v)
                    for neighbor in adjacency_matrix[v]:
                        if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                            dfs(neighbor)

                initial_vertex = next((v for v in adjacency_matrix if any(adjacency_matrix[v].values())), None)
                if not initial_vertex:
                    return False
                dfs(initial_vertex)

                return all(v in visited for v in adjacency_matrix if any(adjacency_matrix[v].values()))

            if not is_weakly_connected():
                self.log_message("O grafo não é fraco-conectado. O grafo não é Euleriano.")
                return False

            return True

        def is_undirected_eulerian():
            self.log_message("Verificando se todos os vértices têm grau par...")

            def is_connected():
                visited = set()
                def dfs(v):
                    visited.add(v)
                    for neighbor in adjacency_matrix[v]:
                        if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                            dfs(neighbor)

                start_vertex = next((v for v in adjacency_matrix if any(adjacency_matrix[v].values())), None)
                if not start_vertex:
                    return False
                dfs(start_vertex)

                return all(v in visited for v in adjacency_matrix if any(adjacency_matrix[v].values()))

            for v in adjacency_matrix:
                degree = sum(1 for neighbor in adjacency_matrix[v] if adjacency_matrix[v][neighbor] != 0)
                self.log_message(f"Vértice {v} tem grau {degree}.")
                if degree % 2 != 0:
                    self.log_message(f"Vértice {v} tem grau ímpar. O grafo não é Euleriano.")
                    return False

            if not is_connected():
                self.log_message("O grafo não é conectado. O grafo não é Euleriano.")
                return False

            self.log_message("Todos os vértices têm grau par e o grafo é conectado.")
            return True

        def hierholzer_algorithm_directed():
            self.log_message("Encontrando o ciclo Euleriano usando o Algoritmo de Hierholzer (Direcionado)...")

            edges = {u: [v for v in adjacency_matrix[u] if adjacency_matrix[u][v] != 0] for u in adjacency_matrix}
            cycle = []
            stack = []
            current = next(iter(edges))

            while edges[current] or stack:
                if not edges[current]:
                    cycle.append(current)
                    current = stack.pop()
                else:
                    stack.append(current)
                    next_vertex = edges[current].pop()
                    current = next_vertex

            cycle.append(current)
            return cycle

        def hierholzer_algorithm():
            self.log_message("Encontrando o ciclo Euleriano usando o Algoritmo de Hierholzer...")

            edges = {u: [v for v in adjacency_matrix[u] if adjacency_matrix[u][v] != 0] for u in adjacency_matrix}
            cycle = []
            stack = []
            current = next(iter(edges))

            while edges[current] or stack:
                if not edges[current]:
                    cycle.append(current)
                    current = stack.pop()
                else:
                    stack.append(current)
                    next_vertex = edges[current].pop()
                    edges[next_vertex].remove(current)
                    current = next_vertex

            cycle.append(current)
            return cycle

        if is_directed():
            if is_directed_eulerian():
                self.log_message("O grafo direcionado é Euleriano.")
                cycle = hierholzer_algorithm_directed()
                cycle_str = " -> ".join(cycle)
                self.log_message(f"Ciclo Euleriano encontrado: {cycle_str}")
                messagebox.showinfo("Grafo Euleriano", f"O grafo direcionado é Euleriano.\nCiclo Euleriano: {cycle_str}")
            else:
                self.log_message("O grafo direcionado não é Euleriano.")
                messagebox.showerror("Não é Euleriano", "O grafo direcionado não é Euleriano.")
        else:
            eulerian = is_undirected_eulerian()
            if eulerian:
                self.log_message("O grafo não direcionado é Euleriano.")
                cycle = hierholzer_algorithm()
                cycle_str = " -> ".join(cycle)
                self.log_message(f"Ciclo Euleriano encontrado: {cycle_str}")
                messagebox.showinfo("Grafo Euleriano", f"O grafo não direcionado é Euleriano.\nCiclo Euleriano: {cycle_str}")
            else:
                self.log_message("O grafo não direcionado não é Euleriano.")
                messagebox.showerror("Não é Euleriano", "O grafo não direcionado não é Euleriano.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()
