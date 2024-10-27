import tkinter as tk
from tkinter import messagebox, simpledialog
from collections import deque
import heapq
import json
import os

class VerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Verifications")
        self.graph_data = {}
        self.graph_names = []
        self.load_graphs()
        self.create_widgets()

    def load_graphs(self):
        if not os.path.exists("adjacency_matrix.json"):
            messagebox.showerror("Error", "No adjacency_matrix.json file found.")
            self.root.destroy()
            return
        with open("adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        self.graph_names = list(self.graph_data.keys())

    def create_widgets(self):
        tk.Label(self.root, text="Select a graph for verification:").pack()
        self.selected_graph = tk.StringVar(value="Choose a graph")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()
        
        self.log_text = tk.Text(self.root, height=15, width=50)
        self.log_text.pack()
        
        tk.Button(self.root, text="Check Edge Existence", command=self.check_edge).pack()
        tk.Button(self.root, text="Check Vertex Degree", command=self.check_vertex_degree).pack()
        tk.Button(self.root, text="Check Vertex Adjacency", command=self.check_vertex_adjacency).pack()
        tk.Button(self.root, text="Check Independent Vertex Set", command=self.check_independent_set).pack()
        tk.Button(self.root, text="Check Clique", command=self.check_clique).pack()
        tk.Button(self.root, text="Check Dominating Set", command=self.check_dominating_set).pack()
        tk.Button(self.root, text="Find Shortest Path", command=self.find_shortest_path).pack()
        tk.Button(self.root, text="Find Lowest Cost Path", command=self.find_lowest_cost_path).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Choose a graph" or graph_name not in self.graph_data:
            messagebox.showerror("Error", "Please select a valid graph name.")
            return None
        return self.graph_data[graph_name]
    
    def check_edge(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return
        vertex1 = simpledialog.askstring("Vertex", "Enter the starting vertex of the edge:")
        vertex2 = simpledialog.askstring("Vertex", "Enter the ending vertex of the edge:")
        if vertex1 and vertex2:
            self.check_edge_existence(graph_info, vertex1, vertex2)
    
    def check_edge_existence(self, graph_info, vertex1, vertex2):
        adjacency_matrix = graph_info['adjacency_matrix']
        if vertex1 in adjacency_matrix and vertex2 in adjacency_matrix[vertex1] and adjacency_matrix[vertex1][vertex2] != 0:
            messagebox.showinfo("Edge Existence", f"The edge ({vertex1} - {vertex2}) exists with weight {adjacency_matrix[vertex1][vertex2]}.")
        else:
            messagebox.showinfo("Edge Existence", f"The edge ({vertex1} - {vertex2}) does not exist.")

    def check_vertex_degree(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return
        vertex = simpledialog.askstring("Vertex", "Enter the vertex:")
        if vertex:
            adjacency_matrix = graph_info['adjacency_matrix']
            if vertex in adjacency_matrix:
                degree = sum(1 for v in adjacency_matrix[vertex] if adjacency_matrix[vertex][v] != 0)
                messagebox.showinfo("Vertex Degree", f"The degree of vertex {vertex} is {degree}.")
            else:
                messagebox.showerror("Error", f"Vertex {vertex} does not exist in the graph.")

    def check_vertex_adjacency(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        vertex = simpledialog.askstring("Vertex", "Enter the vertex to check adjacency:")

        if vertex:
            adjacency_matrix = graph_info['adjacency_matrix']
            if vertex in adjacency_matrix:
                adjacent_vertices = [v for v in adjacency_matrix[vertex] if adjacency_matrix[vertex][v] != 0]
                if adjacent_vertices:
                    messagebox.showinfo("Vertex Adjacency", f"Vertices adjacent to {vertex}: {', '.join(adjacent_vertices)}.")
                else:
                    messagebox.showinfo("Vertex Adjacency", f"Vertex {vertex} has no adjacent vertices.")
            else:
                messagebox.showerror("Error", f"Vertex {vertex} does not exist in the graph.")

    def check_independent_set(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Starting independent set verification...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        vertices_input = simpledialog.askstring("Input", "Enter the set of vertices (comma separated):")
        if not vertices_input:
            self.log_message("No vertices provided.")
            return

        vertices = vertices_input.split(',')
        vertices = [v.strip() for v in vertices]

        for i, v1 in enumerate(vertices):
            for v2 in vertices[i+1:]:
                if v1 in adjacency_matrix and v2 in adjacency_matrix[v1] and adjacency_matrix[v1][v2] != 0:
                    self.log_message(f"Vertices {v1} and {v2} are adjacent. The set is not independent.")
                    messagebox.showerror("Not Independent Set", f"Vertices {v1} and {v2} are adjacent. The set is not independent.")
                    return

        self.log_message("The set is independent.")
        messagebox.showinfo("Independent Set", "The set is independent.")

    def check_clique(self):
        self.log_text.delete(1.0, tk.END)  # Limpar o log anterior
        self.log_message("Starting clique verification...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        vertices_input = simpledialog.askstring("Input", "Enter the set of vertices (comma separated):")
        if not vertices_input:
            self.log_message("No vertices provided.")
            return

        vertices = vertices_input.split(',')
        vertices = [v.strip() for v in vertices]

        for i, v1 in enumerate(vertices):
            for v2 in vertices[i+1:]:
                if v1 in adjacency_matrix and v2 in adjacency_matrix[v1] and adjacency_matrix[v1][v2] == 0:
                    self.log_message(f"Vertices {v1} and {v2} are not adjacent. The set is not a clique.")
                    messagebox.showerror("Not a Clique", f"Vertices {v1} and {v2} are not adjacent. The set is not a clique.")
                    return
                elif v1 not in adjacency_matrix or v2 not in adjacency_matrix[v1]:
                    self.log_message(f"Vertices {v1} and {v2} are not adjacent. The set is not a clique.")
                    messagebox.showerror("Not a Clique", f"Vertices {v1} and {v2} are not adjacent. The set is not a clique.")
                    return

        self.log_message("The set is a clique.")
        messagebox.showinfo("Clique", "The set is a clique.")

    def check_dominating_set(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Starting verification of specified dominating set...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        all_vertices = set(adjacency_matrix.keys())

        vertices_input = simpledialog.askstring("Input", "Enter the set of vertices (comma separated):")
        if not vertices_input:
            self.log_message("No vertices provided.")
            return

        test_set = {v.strip() for v in vertices_input.split(',')}
        
        covered_vertices = set(test_set)

        for vertex in test_set:
            if vertex in adjacency_matrix:
                for neighbor in adjacency_matrix[vertex]:
                    if adjacency_matrix[vertex][neighbor] != 0:
                        covered_vertices.add(neighbor)

        if covered_vertices == all_vertices:
            for vertex in test_set:
                temp_set = test_set - {vertex}
                temp_covered = set(temp_set)
                for v in temp_set:
                    if v in adjacency_matrix:
                        for neighbor in adjacency_matrix[v]:
                            if adjacency_matrix[v][neighbor] != 0:
                                temp_covered.add(neighbor)
                if temp_covered == all_vertices:
                    self.log_message(f"The specified set {test_set} is not minimal.")
                    messagebox.showerror("Not a Minimal Dominating Set", f"The specified set {test_set} is not minimal.")
                    return
            self.log_message(f"The specified set {test_set} is a minimal dominating set.")
            messagebox.showinfo("Minimal Dominating Set", f"The specified set {test_set} is a minimal dominating set.")
        else:
            missing_vertices = all_vertices - covered_vertices
            self.log_message(f"The specified set is not a dominating set. Missing vertices: {', '.join(missing_vertices)}.")
            messagebox.showerror("Not a Dominating Set", f"The specified set is not a dominating set. Missing vertices: {', '.join(missing_vertices)}.")

    def find_shortest_path(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        start_vertex = simpledialog.askstring("Input", "Enter the starting vertex:")
        end_vertex = simpledialog.askstring("Input", "Enter the ending vertex:")

        if start_vertex not in adjacency_matrix or end_vertex not in adjacency_matrix:
            messagebox.showerror("Error", "One or both vertices do not exist in the graph.")
            return

        path = self.bfs_shortest_path(adjacency_matrix, start_vertex, end_vertex)
        if path:
            self.log_message(f"Shortest path from {start_vertex} to {end_vertex}: " + " -> ".join(path))
            messagebox.showinfo("Shortest Path", f"Shortest path from {start_vertex} to {end_vertex}: " + " -> ".join(path))
        else:
            self.log_message(f"No path exists between {start_vertex} and {end_vertex}.")
            messagebox.showerror("No Path", f"No path exists between {start_vertex} and {end_vertex}.")

    def bfs_shortest_path(self, adjacency_matrix, start, goal):
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            vertex = path[-1]

            if vertex == goal:
                return path

            elif vertex not in visited:
                for neighbor in adjacency_matrix[vertex]:
                    if adjacency_matrix[vertex][neighbor] != 0:
                        new_path = list(path)
                        new_path.append(neighbor)
                        queue.append(new_path)

                visited.add(vertex)

        return None

    def find_lowest_cost_path(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        if not graph_info.get('has_weights', False):
            messagebox.showerror("Error", "This function only works for weighted graphs.")
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        start_vertex = simpledialog.askstring("Input", "Enter the starting vertex:")
        end_vertex = simpledialog.askstring("Input", "Enter the ending vertex:")

        if start_vertex not in adjacency_matrix or end_vertex not in adjacency_matrix:
            messagebox.showerror("Error", "One or both vertices do not exist in the graph.")
            return

        path, cost = self.dijkstra_shortest_path(adjacency_matrix, start_vertex, end_vertex)
        if path:
            self.log_message(f"Lowest cost path from {start_vertex} to {end_vertex}: " + " -> ".join(path) + f" with cost {cost}")
            messagebox.showinfo("Lowest Cost Path", f"Lowest cost path from {start_vertex} to {end_vertex}: " + " -> ".join(path) + f" with cost {cost}")
        else:
            self.log_message(f"No path exists between {start_vertex} and {end_vertex}.")
            messagebox.showerror("No Path", f"No path exists between {start_vertex} and {end_vertex}.")

    def dijkstra_shortest_path(self, adjacency_matrix, start, goal):
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
                return path, current_cost

            for neighbor, weight in adjacency_matrix[current_vertex].items():
                if weight > 0 and neighbor not in visited:
                    new_cost = current_cost + weight
                    if new_cost < min_costs[neighbor]:
                        min_costs[neighbor] = new_cost
                        heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))

        return None, float('inf')

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()