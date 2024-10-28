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
        
        self.log_text = tk.Text(self.root, height=20, width=70)
        self.log_text.pack()
        
        tk.Button(self.root, text="Verificar se o Grafo é Cíclico", command=self.check_if_cyclic).pack(pady=20)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_if_cyclic(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        vertices = list(adjacency_matrix.keys())
        visited = set()
        visiting = set()
        cycle_vertices = set()

        def has_cycle(v):
            self.log_message(f"Verificando o vértice: {v}")
            if v in visiting:
                self.log_message(f"Vértice {v} está em 'visiting', ciclo encontrado!")
                return True
            if v in visited:
                self.log_message(f"Vértice {v} já foi visitado, pulando.")
                return False

            visiting.add(v)
            self.log_message(f"Adicionando {v} a 'visiting'.")
            for neighbor in adjacency_matrix[v]:
                if adjacency_matrix[v][neighbor] != 0:
                    self.log_message(f"Vértice {v} tem vizinho: {neighbor}.")
                    if has_cycle(neighbor):
                        cycle_vertices.add(v)
                        self.log_message(f"Vértice {v} está envolvido em um ciclo.")
                        return True
            
            visiting.remove(v)
            visited.add(v)
            self.log_message(f"Marcando {v} como visitado.")
            return False

        cycle_count = 0

        for vertex in vertices:
            if vertex not in visited:
                self.log_message(f"Iniciando verificação para o vértice: {vertex}.")
                if has_cycle(vertex):
                    cycle_count += 1

        total_vertices = len(vertices)

        if cycle_count > 0:
            messagebox.showinfo("Verificação Cíclica do Grafo", 
                f"O grafo contém {cycle_count} ciclo(s).\n"
                f"Vértices envolvidos em ciclo(s): {', '.join(cycle_vertices)}.")
        else:
            messagebox.showinfo("Verificação Cíclica do Grafo", 
                f"O grafo não contém um ciclo.\nTotal de vértices: {total_vertices}.")
            
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = VerificationApp(root)
    root.mainloop()