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
        
        tk.Button(self.root, text="Verificar Componentes Fortemente Conectados", command=self.check_strongly_connected_components).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_strongly_connected_components(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Iniciando a verificação de componentes fortemente conectados...")

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

        if not is_directed():
            messagebox.showerror("Erro", "O grafo não é direcionado. Componentes fortemente conectados se aplicam apenas a grafos direcionados.")
            return

        def dfs(v, visited, stack=None):
            visited.add(v)
            for neighbor in adjacency_matrix[v]:
                if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                    dfs(neighbor, visited, stack)
            if stack is not None:
                stack.append(v)

        def transpose_graph():
            transposed = {v: {} for v in adjacency_matrix}
            for u in adjacency_matrix:
                for v in adjacency_matrix[u]:
                    if adjacency_matrix[u][v] != 0:
                        transposed[v][u] = adjacency_matrix[u][v]
            return transposed

        visited = set()
        stack = []
        for vertex in adjacency_matrix:
            if vertex not in visited:
                self.log_message(f"Executando DFS a partir do vértice: {vertex}")
                dfs(vertex, visited, stack)

        transposed_graph = transpose_graph()
        self.log_message("Grafo transposto criado.")

        visited.clear()
        strongly_connected_components = []
        
        def dfs_on_transposed(v, visited, component):
            visited.add(v)
            component.append(v)
            for neighbor in transposed_graph[v]:
                if transposed_graph[v][neighbor] != 0 and neighbor not in visited:
                    dfs_on_transposed(neighbor, visited, component)

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                component = []
                self.log_message(f"Executando DFS no grafo transposto a partir do vértice: {vertex}")
                dfs_on_transposed(vertex, visited, component)
                strongly_connected_components.append(component)

        num_components = len(strongly_connected_components)
        component_info = "\n".join([f"Componente {i+1}: {', '.join(component)}" for i, component in enumerate(strongly_connected_components)])

        self.log_message(f"Número de componentes fortemente conectados: {num_components}")
        self.log_message(component_info)

        messagebox.showinfo("Componentes Fortemente Conectados", 
            f"Número de componentes fortemente conectados: {num_components}\n\n{component_info}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()