import tkinter as tk
from tkinter import messagebox, simpledialog
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
        
        tk.Button(self.root, text="Verificar Conjunto Dominante", command=self.check_dominating_set).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_dominating_set(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Iniciando verificação do conjunto dominante especificado...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        all_vertices = set(adjacency_matrix.keys())

        vertices_input = simpledialog.askstring("Entrada", "Digite o conjunto de vértices (separados por vírgula):")
        if not vertices_input:
            self.log_message("Nenhum vértice fornecido.")
            return

        test_set = {v.strip() for v in vertices_input.split(',')}
        self.log_message(f"Conjunto de vértices fornecido: {test_set}")
        
        covered_vertices = set(test_set)

        for vertex in test_set:
            if vertex in adjacency_matrix:
                for neighbor in adjacency_matrix[vertex]:
                    if adjacency_matrix[vertex][neighbor] != 0:
                        covered_vertices.add(neighbor)

        if covered_vertices == all_vertices:
            self.log_message("O conjunto especificado cobre todos os vértices.")
            for vertex in test_set:
                temp_set = test_set - {vertex}
                temp_covered = set(temp_set)
                for v in temp_set:
                    if v in adjacency_matrix:
                        for neighbor in adjacency_matrix[v]:
                            if adjacency_matrix[v][neighbor] != 0:
                                temp_covered.add(neighbor)
                if temp_covered == all_vertices:
                    self.log_message(f"O conjunto especificado {test_set} não é minimal.")
                    messagebox.showerror("Não é um Conjunto Dominante Minimal", f"O conjunto especificado {test_set} não é minimal.")
                    return
            self.log_message(f"O conjunto especificado {test_set} é um conjunto dominante minimal.")
            messagebox.showinfo("Conjunto Dominante Minimal", f"O conjunto especificado {test_set} é um conjunto dominante minimal.")
        else:
            missing_vertices = all_vertices - covered_vertices
            self.log_message(f"O conjunto especificado não é um conjunto dominante. Vértices faltando: {', '.join(missing_vertices)}.")
            messagebox.showerror("Não é um Conjunto Dominante", f"O conjunto especificado não é um conjunto dominante. Vértices faltando: {', '.join(missing_vertices)}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()