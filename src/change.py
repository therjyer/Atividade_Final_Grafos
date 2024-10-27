import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ChangeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Editar Grafos Existentes")
        
        self.graph_data = {}
        self.graph_name = None
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
        tk.Label(self.root, text="Selecione um grafo para editar:").pack()
        
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()

        tk.Button(self.root, text="Renomear Grafo", command=self.rename_graph).pack()
        tk.Button(self.root, text="Mudar Tipo de Grafo", command=self.change_graph_type).pack()
        tk.Button(self.root, text="Adicionar/Remover Vértice", command=self.modify_vertices).pack()
        tk.Button(self.root, text="Renomear Vértice", command=self.rename_vertex).pack()
        tk.Button(self.root, text="Mudar Vértices da Aresta", command=self.change_edge_vertices).pack()
        tk.Button(self.root, text="Mudar Peso da Aresta", command=self.change_edge_weight).pack()

    def get_graph_info(self):
        self.graph_name = self.selected_graph.get()
        if self.graph_name == "Escolha um grafo" or self.graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um grafo válido.")
            return None
        return self.graph_data[self.graph_name]

    def save_changes(self):
        with open("../lib/adjacency_matrix.json", "w") as f:
            json.dump(self.graph_data, f, indent=4)
        messagebox.showinfo("Salvo", "Alterações salvas em adjacency_matrix.json")

    def rename_graph(self):
        self.graph_name = self.selected_graph.get()
        if self.graph_name == "Escolha um grafo" or self.graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um grafo válido para renomear.")
            return

        new_name = simpledialog.askstring("Renomear Grafo", "Digite um novo nome para o grafo:")
        if new_name:
            if new_name in self.graph_data:
                messagebox.showerror("Erro", "Já existe um grafo com esse nome.")
                return
            self.graph_data[new_name] = self.graph_data.pop(self.graph_name)
            self.graph_name = new_name
            self.selected_graph.set(new_name)
            self.save_changes()

    def change_graph_type(self):
        graph_info = self.get_graph_info()
        if graph_info:
            new_type = "não direcionado" if graph_info["type"] == "direcionado" else "direcionado"
            graph_info["type"] = new_type
            self.save_changes()

    def modify_vertices(self):
        graph_info = self.get_graph_info()
        if graph_info:
            choice = messagebox.askyesno("Modificar Vértices", "Você gostaria de adicionar um vértice?")
            if choice:
                new_vertex = simpledialog.askstring("Adicionar Vértice", "Digite o nome do novo vértice:")
                if new_vertex and new_vertex not in graph_info["adjacency_matrix"]:
                    graph_info["adjacency_matrix"][new_vertex] = {v: 0 for v in graph_info["adjacency_matrix"]}
                    for v in graph_info["adjacency_matrix"]:
                        graph_info["adjacency_matrix"][v][new_vertex] = 0
            else:
                remove_vertex = simpledialog.askstring("Remover Vértice", "Digite o nome do vértice a ser removido:")
                if remove_vertex and remove_vertex in graph_info["adjacency_matrix"]:
                    del graph_info["adjacency_matrix"][remove_vertex]
                    for v in graph_info["adjacency_matrix"]:
                        if remove_vertex in graph_info["adjacency_matrix"][v]:
                            del graph_info["adjacency_matrix"][v][remove_vertex]
            self.save_changes()

    def rename_vertex(self):
        graph_info = self.get_graph_info()
        if graph_info:
            old_vertex = simpledialog.askstring("Renomear Vértice", "Digite o nome do vértice a ser renomeado:")
            if old_vertex and old_vertex in graph_info["adjacency_matrix"]:
                new_vertex = simpledialog.askstring("Novo Nome do Vértice", "Digite o novo nome para o vértice:")
                if new_vertex and new_vertex not in graph_info["adjacency_matrix"]:
                    graph_info["adjacency_matrix"][new_vertex] = graph_info["adjacency_matrix"].pop(old_vertex)
                    for v in graph_info["adjacency_matrix"]:
                        if old_vertex in graph_info["adjacency_matrix"][v]:
                            graph_info["adjacency_matrix"][v][new_vertex] = graph_info["adjacency_matrix"][v].pop(old_vertex)
                    self.save_changes()
                else:
                    messagebox.showerror("Erro", "O novo nome do vértice já existe ou é inválido.")
            else:
                messagebox.showerror("Erro", "Vértice não encontrado.")

    def change_edge_vertices(self):
        graph_info = self.get_graph_info()
        if graph_info:
            old_edge = simpledialog.askstring("Mudar Aresta", "Digite a aresta (ex: A-B):")
            if old_edge:
                v1, v2 = old_edge.split("-")
                if v1 in graph_info["adjacency_matrix"] and v2 in graph_info["adjacency_matrix"][v1]:
                    new_v1 = simpledialog.askstring("Novo Origem", "Digite o novo vértice de origem:")
                    new_v2 = simpledialog.askstring("Nova Destino", "Digite o novo vértice de destino:")
                    if new_v1 and new_v2:
                        weight = graph_info["adjacency_matrix"][v1].pop(v2)
                        if v1 in graph_info["adjacency_matrix"] and new_v1 in graph_info["adjacency_matrix"]:
                            graph_info["adjacency_matrix"][new_v1][new_v2] = weight
            self.save_changes()

    def change_edge_weight(self):
        graph_info = self.get_graph_info()
        if graph_info:
            edge = simpledialog.askstring("Mudar Peso da Aresta", "Digite a aresta (ex: A-B):")
            if edge:
                v1, v2 = edge.split("-")
                if v1 in graph_info["adjacency_matrix"] and v2 in graph_info["adjacency_matrix"][v1]:
                    new_weight = simpledialog.askinteger("Novo Peso", f"Digite o novo peso para a aresta {v1}-{v2}:")
                    if new_weight is not None:
                        graph_info["adjacency_matrix"][v1][v2] = new_weight
                        if graph_info["type"] == "não direcionado":
                            graph_info["adjacency_matrix"][v2][v1] = new_weight
            self.save_changes()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChangeGraphApp(root)
    root.mainloop()
