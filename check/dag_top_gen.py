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
        
        tk.Button(self.root, text="Gerar uma Ordenação Topológica em um DAG", command=self.check_dag_and_topological_sort).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_dag_and_topological_sort(self):
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

        def is_acyclic():
            visited = set()
            recursion_stack = set()

            def dfs(v):
                visited.add(v)
                recursion_stack.add(v)
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0:
                        if neighbor not in visited:
                            if dfs(neighbor):
                                return True
                        elif neighbor in recursion_stack:
                            return True
                recursion_stack.remove(v)
                return False

            for vertex in adjacency_matrix:
                if vertex not in visited:
                    if dfs(vertex):
                        return False
            return True

        def topological_sort():
            visited = set()
            stack = []

            def dfs(v):
                visited.add(v)
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                        dfs(neighbor)
                stack.append(v)

            for vertex in adjacency_matrix:
                if vertex not in visited:
                    dfs(vertex)

            return stack[::-1]

        if is_directed():
            if is_acyclic():
                topo_sort = topological_sort()
                messagebox.showinfo("DAG e Ordenação Topológica", 
                    f"O grafo é um grafo acíclico direcionado (DAG).\nOrdem Topológica: {', '.join(topo_sort)}")
            else:
                messagebox.showerror("Grafo Cíclico", "O grafo é direcionado, mas contém um ciclo, portanto não é um DAG.")
        else:
            messagebox.showerror("Não é um Grafo Direcionado", "O grafo não é direcionado.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()
