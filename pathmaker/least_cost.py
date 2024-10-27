import tkinter as tk
from tkinter import messagebox, simpledialog
import heapq
import json
import os

class VerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificações de Grafos")
        self.graph_data = {}
        self.graph_names = []
        self.log_message("Inicializando o aplicativo...")
        self.load_graphs()
        self.create_widgets()

    def load_graphs(self):
        self.log_message("Carregando grafos do arquivo...")
        if not os.path.exists("../lib/adjacency_matrix.json"):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            self.root.destroy()
            return
        with open("../lib/adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        self.graph_names = list(self.graph_data.keys())
        self.log_message(f"Grafo(s) carregado(s): {self.graph_names}")

    def create_widgets(self):
        tk.Label(self.root, text="Selecione um grafo para verificação:").pack()
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()
        
        self.log_text = tk.Text(self.root, height=15, width=50)
        self.log_text.pack()
        
        tk.Button(self.root, text="Encontrar Caminho de Menor Custo", command=self.find_lowest_cost_path).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        print(message)  # Exibe no console também

    def get_selected_graph(self):
        self.log_message("Obtendo grafo selecionado...")
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        self.log_message(f"Grafo selecionado: {graph_name}")
        return self.graph_data[graph_name]

    def find_lowest_cost_path(self):
        self.log_message("Iniciando a busca pelo caminho de menor custo...")
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        if not graph_info.get('has_weights', False):
            messagebox.showerror("Erro", "Esta função só funciona para grafos com pesos.")
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        start_vertex = simpledialog.askstring("Entrada", "Digite o vértice de partida:")
        end_vertex = simpledialog.askstring("Entrada", "Digite o vértice de chegada:")
        
        self.log_message(f"Vértice de partida: {start_vertex}, Vértice de chegada: {end_vertex}")

        if start_vertex not in adjacency_matrix or end_vertex not in adjacency_matrix:
            messagebox.showerror("Erro", "Um ou ambos os vértices não existem no grafo.")
            return

        if self.has_negative_cycle(adjacency_matrix, start_vertex):
            self.log_message("O grafo tem um ciclo negativo. Usando Bellman-Ford para o caminho mais curto.")
            path, cost = self.bellman_ford_shortest_path(adjacency_matrix, start_vertex, end_vertex)
        else:
            self.log_message("Usando Dijkstra para o caminho mais curto.")
            path, cost = self.dijkstra_shortest_path(adjacency_matrix, start_vertex, end_vertex)

        if path:
            self.log_message(f"Caminho de menor custo encontrado: " + " -> ".join(path) + f" com custo {cost}")
            messagebox.showinfo("Caminho de Menor Custo", f"Caminho de menor custo de {start_vertex} para {end_vertex}: " + " -> ".join(path) + f" com custo {cost}")
        else:
            self.log_message(f"Nenhum caminho existe entre {start_vertex} e {end_vertex}.")
            messagebox.showerror("Nenhum Caminho", f"Nenhum caminho existe entre {start_vertex} e {end_vertex}.")

    def has_negative_cycle(self, adjacency_matrix, start):
        self.log_message("Verificando se o grafo tem ciclos negativos...")
        min_costs = {vertex: float('inf') for vertex in adjacency_matrix}
        min_costs[start] = 0

        vertices = list(adjacency_matrix.keys())
        for _ in range(len(vertices) - 1):
            for u in adjacency_matrix:
                for v, weight in adjacency_matrix[u].items():
                    if weight != 0 and min_costs[u] != float('inf') and min_costs[u] + weight < min_costs[v]:
                        min_costs[v] = min_costs[u] + weight

        for u in adjacency_matrix:
            for v, weight in adjacency_matrix[u].items():
                if weight != 0 and min_costs[u] != float('inf') and min_costs[u] + weight < min_costs[v]:
                    self.log_message("Ciclo negativo encontrado.")
                    return True

        self.log_message("Nenhum ciclo negativo encontrado.")
        return False

    def bellman_ford_shortest_path(self, adjacency_matrix, start, goal):
        self.log_message("Executando Bellman-Ford...")
        min_costs = {vertex: float('inf') for vertex in adjacency_matrix}
        predecessors = {vertex: None for vertex in adjacency_matrix}
        min_costs[start] = 0

        vertices = list(adjacency_matrix.keys())
        for _ in range(len(vertices) - 1):
            for u in adjacency_matrix:
                for v, weight in adjacency_matrix[u].items():
                    if weight != 0 and min_costs[u] != float('inf') and min_costs[u] + weight < min_costs[v]:
                        min_costs[v] = min_costs[u] + weight
                        predecessors[v] = u

        if min_costs[goal] == float('inf'):
            self.log_message("Nenhum caminho encontrado com Bellman-Ford.")
            return None, float('inf')

        path = []
        current = goal
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]

        self.log_message(f"Caminho encontrado com Bellman-Ford: {path}, Custo: {min_costs[goal]}")
        return path, min_costs[goal]

    def dijkstra_shortest_path(self, adjacency_matrix, start, goal):
        self.log_message("Executando Dijkstra...")
        min_costs = {vertex: float('inf') for vertex in adjacency_matrix}
        min_costs[start] = 0
        priority_queue = [(0, start, [start])]
        visited = set()

        while priority_queue:
            current_cost, current_vertex, path = heapq.heappop(priority_queue)

            if current_vertex in visited:
                continue

            visited.add(current_vertex)

            if current_vertex == goal:
                self.log_message(f"Caminho encontrado com Dijkstra: {path}, Custo: {current_cost}")
                return path, current_cost

            for neighbor, weight in adjacency_matrix[current_vertex].items():
                if weight > 0 and neighbor not in visited:
                    new_cost = current_cost + weight
                    if new_cost < min_costs[neighbor]:
                        min_costs[neighbor] = new_cost
                        heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))

        self.log_message("Nenhum caminho encontrado com Dijkstra.")
        return None, float('inf')

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()