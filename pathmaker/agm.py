import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import messagebox
import json
import os

class VerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificações de Grafos")
        self.graph_data = {}
        self.graph_names = []

        self.log_text = tk.Text(self.root, height=20, width=70)
        self.log_text.pack()

        self.load_graphs()
        self.create_widgets()

    def load_graphs(self):
        self.log_message("Tentando carregar grafos do arquivo...")
        if not os.path.exists("../lib/adjacency_matrix.json"):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            self.log_message("Erro: Arquivo não encontrado.")
            self.root.destroy()
            return
        with open("../lib/adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        self.graph_names = list(self.graph_data.keys())
        self.log_message(f"{len(self.graph_names)} grafos carregados com sucesso.")

    def create_widgets(self):
        tk.Label(self.root, text="Selecione um grafo para verificação:").pack()
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()

        tk.Label(self.root, text="Escolha o vértice inicial:").pack()
        self.start_vertex = tk.StringVar()
        self.start_vertex_entry = tk.Entry(self.root, textvariable=self.start_vertex)
        self.start_vertex_entry.pack()

        tk.Button(self.root, text="Encontrar Árvore Geradora Mínima (AGM)", command=self.find_mst).pack(pady=20)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        self.log_message(f"Grafo selecionado: {graph_name}.")
        return self.graph_data[graph_name]

    def find_mst(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        start_vertex = self.start_vertex.get()
        if not start_vertex:
            messagebox.showerror("Erro", "Por favor, insira um vértice inicial.")
            return

        if not graph_info.get('has_weights', False) or graph_info.get('type') != "undirected":
            messagebox.showerror("Erro", "A AGM só pode ser encontrada para grafos não direcionados com pesos.")
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        self.log_message("Iniciando a busca pela Árvore Geradora Mínima...")
        mst, total_weight, selected_vertices, predecessors = self.kruskal_mst(adjacency_matrix, start_vertex)

        if mst:
            edges = [f"{u}-{v} (peso {w})" for u, v, w in mst]
            self.log_message("Árvore Geradora Mínima encontrada com peso total: " + str(total_weight))
            self.log_message("Arestas na AGM:\n" + "\n".join(edges))
            self.log_message("Vértices selecionados: " + ", ".join(selected_vertices))
            self.log_message("Antecessores: " + ", ".join([f"{v}: {p}" for v, p in predecessors.items()]))
            messagebox.showinfo("AGM", "Árvore Geradora Mínima encontrada:\n" + "\n".join(edges) + f"\nPeso Total: {total_weight}")
        else:
            self.log_message("Nenhuma AGM encontrada.")
            messagebox.showerror("AGM", "Nenhuma AGM encontrada.")
    
        self.draw_mst(mst)

    def kruskal_mst(self, adjacency_matrix, start_vertex):
        edges = []
        for u in adjacency_matrix:
            for v, weight in adjacency_matrix[u].items():
                if u < v and weight > 0:
                    edges.append((weight, u, v))

        edges.sort()
        mst = []
        total_weight = 0

        parent = {}
        rank = {}
        selected_vertices = []
        predecessors = {}

        def find(vertex):
            if parent[vertex] != vertex:
                parent[vertex] = find(parent[vertex])
            return parent[vertex]

        def union(vertex1, vertex2):
            root1 = find(vertex1)
            root2 = find(vertex2)
            if root1 != root2:
                if rank[root1] > rank[root2]:
                    parent[root2] = root1
                elif rank[root1] < rank[root2]:
                    parent[root1] = root2
                else:
                    parent[root2] = root1
                    rank[root1] += 1

        for vertex in adjacency_matrix:
            parent[vertex] = vertex
            rank[vertex] = 0

        if start_vertex in adjacency_matrix:
            selected_vertices.append(start_vertex)
            for weight, u, v in edges:
                if find(u) != find(v):
                    union(u, v)
                    mst.append((u, v, weight))
                    total_weight += weight
                    selected_vertices.append(u)
                    selected_vertices.append(v)
                    predecessors[v] = u
        else:
            self.log_message(f"Vértice inicial {start_vertex} não existe no grafo.")
            return [], 0, [], {}

        return mst, total_weight, list(set(selected_vertices)), predecessors

    def draw_mst(self, mst):
        G = nx.Graph()
        for u, v, weight in mst:
            G.add_edge(u, v, weight=weight)

        pos = nx.spring_layout(G)
        edge_labels = {(u, v): f"{weight}" for u, v, weight in mst}

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")
        plt.title("Árvore Geradora Mínima (AGM)")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = VerificationApp(root)
    root.mainloop()