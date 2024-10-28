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
        
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.create_widgets()
        self.load_graphs()

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
        self.update_graph_menu()
        self.log_message(f"{len(self.graph_names)} grafos carregados com sucesso.")

    def create_widgets(self):
        tk.Label(self.root, text="Selecione um grafo para verificação:").pack()
        
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, "Escolha um grafo")
        self.graph_menu.pack()
        
        self.log_text = tk.Text(self.root, height=20, width=70)
        self.log_text.pack()
        
        tk.Button(self.root, text="Encontrar Caminho de Menor Custo", command=self.find_lowest_cost_path).pack(pady=20)

    def update_graph_menu(self):
        menu = self.graph_menu["menu"]
        menu.delete(0, "end")
        for graph_name in self.graph_names:
            menu.add_command(label=graph_name, command=lambda value=graph_name: self.selected_graph.set(value))
        self.selected_graph.set(self.graph_names[0] if self.graph_names else "Escolha um grafo")

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def find_lowest_cost_path(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        if not graph_info.get('has_weights', False):
            messagebox.showerror("Erro", "Esta função só funciona para grafos ponderados.")
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        start_vertex = simpledialog.askstring("Entrada", "Digite o vértice inicial:")
        end_vertex = simpledialog.askstring("Entrada", "Digite o vértice final:")

        if start_vertex not in adjacency_matrix or end_vertex not in adjacency_matrix:
            messagebox.showerror("Erro", "Um ou ambos os vértices não existem no grafo.")
            return

        if self.has_negative_cycle(adjacency_matrix, start_vertex):
            self.log_message("O grafo tem um ciclo negativo. Usando Bellman-Ford para o caminho mais curto.")
            path, cost, predecessors = self.bellman_ford_shortest_path(adjacency_matrix, start_vertex, end_vertex)
        else:
            path, cost, predecessors = self.dijkstra_shortest_path(adjacency_matrix, start_vertex, end_vertex)

        if path:
            self.log_message(f"Caminho de menor custo de {start_vertex} a {end_vertex}: " + " -> ".join(path) + f" com custo {cost}")
            self.log_message("Vértices escolhidos: " + " -> ".join(path))
            self.log_message("Antecessores: " + ", ".join([f"{v}: {p}" for v, p in predecessors.items() if p is not None]))
            messagebox.showinfo("Caminho de Menor Custo", f"Caminho de menor custo de {start_vertex} a {end_vertex}: " + " -> ".join(path) + f" com custo {cost}")
        else:
            self.log_message(f"Nenhum caminho existe entre {start_vertex} e {end_vertex}.")
            messagebox.showerror("Sem Caminho", f"Nenhum caminho existe entre {start_vertex} e {end_vertex}.")

    def has_negative_cycle(self, adjacency_matrix, start):
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
                    return True

        return False

    def bellman_ford_shortest_path(self, adjacency_matrix, start, goal):
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
                        self.log_message(f"Atualizando custo de {v} para {min_costs[v]} (predecessor: {u})")

        if min_costs[goal] == float('inf'):
            return None, float('inf'), {}

        path = []
        current = goal
        while current is not None:
            path.insert(0, current)
            current = predecessors[current]

        return path, min_costs[goal], predecessors

    def dijkstra_shortest_path(self, adjacency_matrix, start, goal):
        min_costs = {vertex: float('inf') for vertex in adjacency_matrix}
        min_costs[start] = 0
        priority_queue = [(0, start, [start])]
        visited = set()
        predecessors = {vertex: None for vertex in adjacency_matrix}

        while priority_queue:
            current_cost, current_vertex, path = heapq.heappop(priority_queue)

            if current_vertex in visited:
                continue

            visited.add(current_vertex)
            self.log_message(f"Visitando {current_vertex} com custo atual {current_cost}")

            if current_vertex == goal:
                return path, current_cost, predecessors

            for neighbor, weight in adjacency_matrix[current_vertex].items():
                if weight > 0 and neighbor not in visited:
                    new_cost = current_cost + weight
                    if new_cost < min_costs[neighbor]:
                        min_costs[neighbor] = new_cost
                        predecessors[neighbor] = current_vertex
                        heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
                        self.log_message(f"Atualizando custo de {neighbor} para {new_cost} (predecessor: {current_vertex})")

        return None, float('inf'), {}

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = VerificationApp(root)
    root.mainloop()