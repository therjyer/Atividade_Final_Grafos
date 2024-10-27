import tkinter as tk 
from tkinter import messagebox, simpledialog
import json
import os

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criador de Grafos")
        
        self.graph_name = None
        self.graph_type = None
        self.has_weights = None
        self.vertices = []
        self.edges = []
        self.adjacency_matrix = {}

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Escolha o Tipo de Grafo:").pack()
        self.graph_type_var = tk.StringVar(value="directed")
        tk.Radiobutton(self.root, text="Dirigido", variable=self.graph_type_var, value="directed").pack()
        tk.Radiobutton(self.root, text="Não Dirigido", variable=self.graph_type_var, value="undirected").pack()

        tk.Button(self.root, text="Próximo", command=self.get_graph_name).pack()

    def get_graph_name(self):
        self.graph_name = simpledialog.askstring("Nome do Grafo", "Digite um nome único para este grafo:")
        if self.graph_name:
            self.get_vertices()

    def get_vertices(self):
        self.graph_type = self.graph_type_var.get()
        vertices_input = simpledialog.askstring("Vértices", "Digite os vértices separados por vírgulas (ex.: A,B,C):")
        if vertices_input:
            self.vertices = [v.strip().upper() for v in vertices_input.split(",")]  # Normalizando para maiúsculas
            self.adjacency_matrix = {v: {u: 0 for u in self.vertices} for v in self.vertices}
            print("Vértices:", self.vertices)  # Debug: Verificação de vértices
            print("Matriz de Adjacência inicial:", self.adjacency_matrix)  # Debug: Verificação da matriz
            self.get_edges()

    def get_edges(self):
        edges_input = simpledialog.askstring("Arestas", "Digite as arestas como pares (ex.: A-B, A-C):")
        if edges_input:
            edges = edges_input.replace(" ", "").split(",")
            for edge in edges:
                v1, v2 = [x.upper() for x in edge.split("-")]  # Normalizando para maiúsculas
                if v1 in self.vertices and v2 in self.vertices:
                    self.edges.append((v1, v2))
            print("Arestas:", self.edges)  # Debug: Verificação de arestas
            self.ask_weights()

    def ask_weights(self):
        response = messagebox.askyesno("Pesos", "O grafo possui pesos?")
        self.has_weights = response
        self.create_adjacency_matrix()

    def create_adjacency_matrix(self):
        for v1, v2 in self.edges:
            print(f"Adicionando aresta {v1}-{v2}")  # Debug: Verificação da aresta sendo adicionada
            if self.has_weights:
                weight = simpledialog.askinteger("Peso", f"Digite o peso para a aresta {v1}-{v2}:")
            else:
                weight = 1        
            self.adjacency_matrix[v1][v2] = weight
            if self.graph_type == "undirected" and v1 != v2:
                self.adjacency_matrix[v2][v1] = weight
        print("Matriz de Adjacência final:", self.adjacency_matrix)  # Debug: Verificação da matriz final
        self.save_to_json()

    def save_to_json(self):
        file_path = "../lib/adjacency_matrix.json"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        graphs = {}
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                graphs = json.load(f)

        if self.graph_name in graphs:
            if messagebox.askyesno("Nome Duplicado", f"O grafo '{self.graph_name}' já existe. Deseja substituir?"):
                del graphs[self.graph_name]
            else:
                messagebox.showinfo("Cancelado", "A criação do grafo foi cancelada.")
                self.root.quit()
                return

        graphs[self.graph_name] = {
            "type": self.graph_type,
            "has_weights": self.has_weights,
            "adjacency_matrix": self.adjacency_matrix
        }

        try:
            with open(file_path, "w") as f:
                json.dump(graphs, f, indent=4)
            messagebox.showinfo("Salvo", f"Grafo '{self.graph_name}' salvo em adjacency_matrix.json")
            self.root.quit()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar o grafo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()