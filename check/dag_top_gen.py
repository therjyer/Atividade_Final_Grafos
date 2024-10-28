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
        tk.Label(self.root, text="Selecione um grafo para verificação:").pack(pady=5)
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack(pady=5)
        
        self.log_text = tk.Text(self.root, height=20, width=70)
        self.log_text.pack(pady=5)
        
        tk.Button(self.root, text="Gerar uma Ordenação Topológica em um DAG", command=self.check_dag_and_topological_sort).pack(pady=20)

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
            self.log_message("Verificando se o grafo é direcionado...")
            for u in adjacency_matrix:
                for v in adjacency_matrix[u]:
                    if adjacency_matrix[u][v] != adjacency_matrix[v].get(u, 0):
                        self.log_message(f"Grafo não é direcionado: {u} -> {v} e {v} não é {u}.")
                        return True
            self.log_message("O grafo é direcionado.")
            return False

        def is_acyclic():
            self.log_message("Verificando se o grafo é acíclico...")
            visited = set()
            recursion_stack = set()

            def dfs(v):
                visited.add(v)
                recursion_stack.add(v)
                self.log_message(f"Visitando vértice: {v}")
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0:
                        if neighbor not in visited:
                            if dfs(neighbor):
                                return True
                        elif neighbor in recursion_stack:
                            self.log_message(f"Ciclo encontrado ao visitar: {neighbor}")
                            return True
                recursion_stack.remove(v)
                return False

            for vertex in adjacency_matrix:
                if vertex not in visited:
                    if dfs(vertex):
                        self.log_message("O grafo contém um ciclo.")
                        return False
            self.log_message("O grafo é acíclico.")
            return True

        def topological_sort():
            self.log_message("Gerando ordenação topológica...")
            visited = set()
            stack = []

            def dfs(v):
                visited.add(v)
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                        dfs(neighbor)
                stack.append(v)
                self.log_message(f"Vértice {v} adicionado à pilha.")

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
    root.geometry("640x480")
    app = VerificationApp(root)
    root.mainloop()