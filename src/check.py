import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
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
        if not os.path.exists("../lib/adjacency_matrix.json"):
            messagebox.showerror("Error", "File not found.")
            self.root.destroy()
            return
        with open("../lib/adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        self.graph_names = list(self.graph_data.keys())

    def create_widgets(self):
        tk.Label(self.root, text="Select a graph for verification:").pack()
        self.selected_graph = tk.StringVar(value="Choose a graph")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()
        
        self.log_text = tk.Text(self.root, height=15, width=50)
        self.log_text.pack()
        
        tk.Button(self.root, text="Check if Graph is Cyclic", command=self.check_if_cyclic).pack()
        tk.Button(self.root, text="Check if Graph is Undirected and Connected", command=self.check_if_undirected_and_connected).pack()
        tk.Button(self.root, text="Check Strongly Connected Components", command=self.check_strongly_connected_components).pack()
        tk.Button(self.root, text="Generate a Topological Sort in a DAG", command=self.check_dag_and_topological_sort).pack()
        tk.Button(self.root, text="Check if Graph is Eulerian", command=self.check_eulerian).pack()
        tk.Button(self.root, text="Check Planarity", command=self.check_planarity).pack()
        tk.Button(self.root, text="Find Minimum Allocation (Hungarian)", command=self.find_minimum_allocation).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Choose a graph" or graph_name not in self.graph_data:
            messagebox.showerror("Error", "Please select a valid graph name.")
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
            if v in visiting:
                return True
            if v in visited:
                return False

            visiting.add(v)
            for neighbor in adjacency_matrix[v]:
                if adjacency_matrix[v][neighbor] != 0:
                    if has_cycle(neighbor):
                        cycle_vertices.add(v)
                        return True
            
            visiting.remove(v)
            visited.add(v)
            return False

        cycle_count = 0

        for vertex in vertices:
            if vertex not in visited:
                if has_cycle(vertex):
                    cycle_count += 1

        total_vertices = len(vertices)

        if cycle_count > 0:
            messagebox.showinfo("Graph Cyclic Check", 
                f"The graph contains {cycle_count} cycle(s).\n"
                f"Vertices involved in cycle(s): {', '.join(cycle_vertices)}.")
        else:
            messagebox.showinfo("Graph Cyclic Check", 
                f"The graph does not contain a cycle.\nTotal vertices: {total_vertices}.")

    def check_if_undirected_and_connected(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        def is_undirected():
            for u in adjacency_matrix:
                for v in adjacency_matrix[u]:
                    if adjacency_matrix[u][v] != adjacency_matrix[v].get(u, 0):
                        return False
            return True

        def is_connected():
            visited = set()
            def dfs(v):
                visited.add(v)
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                        dfs(neighbor)

            initial_vertex = next(iter(adjacency_matrix))
            dfs(initial_vertex)

            return len(visited) == len(adjacency_matrix)

        if is_undirected():
            if is_connected():
                messagebox.showinfo("Graph Check", "The graph is undirected and connected.")
            else:
                messagebox.showinfo("Graph Check", "The graph is undirected but not connected.")
        else:
            messagebox.showinfo("Graph Check", "The graph is directed.")

    def check_strongly_connected_components(self):
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
            messagebox.showerror("Error", "The graph is not directed. Strongly connected components only apply to directed graphs.")
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
                dfs(vertex, visited, stack)

        transposed_graph = transpose_graph()

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
                dfs_on_transposed(vertex, visited, component)
                strongly_connected_components.append(component)

        num_components = len(strongly_connected_components)
        component_info = "\n".join([f"Component {i+1}: {', '.join(component)}" for i, component in enumerate(strongly_connected_components)])

        messagebox.showinfo("Strongly Connected Components", 
            f"Number of strongly connected components: {num_components}\n\n{component_info}")

    def check_dag_and_topological_sort(self):
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

        def is_acyclic():
            visited = set()
            recursion_stack = set()

            def dfs(v):
                visited.add(v)
                recursion_stack.add(v)
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0:
                        if neighbor not in visited:
                            if dfs(neighbor):
                                return True
                        elif neighbor in recursion_stack:
                            return True
                recursion_stack.remove(v)
                return False

            for vertex in adjacency_matrix:
                if vertex not in visited:
                    if dfs(vertex):
                        return False
            return True

        def topological_sort():
            visited = set()
            stack = []

            def dfs(v):
                visited.add(v)
                for neighbor in adjacency_matrix[v]:
                    if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                        dfs(neighbor)
                stack.append(v)

            for vertex in adjacency_matrix:
                if vertex not in visited:
                    dfs(vertex)

            return stack[::-1]

        if is_directed():
            if is_acyclic():
                topo_sort = topological_sort()
                messagebox.showinfo("DAG and Topological Sort", 
                    f"The graph is a directed acyclic graph (DAG).\nTopological Order: {', '.join(topo_sort)}")
            else:
                messagebox.showerror("Cyclic Graph", "The graph is directed but contains a cycle, so it is not a DAG.")
        else:
            messagebox.showerror("Not a Directed Graph", "The graph is not directed.")

    def check_eulerian(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Starting Eulerian graph verification...")

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

        def is_directed_eulerian():
            self.log_message("Checking if all vertices have equal in-degree and out-degree...")

            in_degree = {v: 0 for v in adjacency_matrix}
            out_degree = {v: 0 for v in adjacency_matrix}

            for u in adjacency_matrix:
                for v in adjacency_matrix[u]:
                    if adjacency_matrix[u][v] != 0:
                        out_degree[u] += 1
                        in_degree[v] += 1

            for v in adjacency_matrix:
                self.log_message(f"Vertex {v}: in-degree = {in_degree[v]}, out-degree = {out_degree[v]}.")
                if in_degree[v] != out_degree[v]:
                    self.log_message(f"Vertex {v} does not have equal in-degree and out-degree. The graph is not Eulerian.")
                    return False

            def is_weakly_connected():
                visited = set()
                def dfs(v):
                    visited.add(v)
                    for neighbor in adjacency_matrix[v]:
                        if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                            dfs(neighbor)

                initial_vertex = next((v for v in adjacency_matrix if any(adjacency_matrix[v].values())), None)
                if not initial_vertex:
                    return False
                dfs(initial_vertex)

                return all(v in visited for v in adjacency_matrix if any(adjacency_matrix[v].values()))

            if not is_weakly_connected():
                self.log_message("The graph is not weakly connected. The graph is not Eulerian.")
                return False

            return True

        def is_undirected_eulerian():
            self.log_message("Checking if all vertices have an even degree...")

            def is_connected():
                visited = set()
                def dfs(v):
                    visited.add(v)
                    for neighbor in adjacency_matrix[v]:
                        if adjacency_matrix[v][neighbor] != 0 and neighbor not in visited:
                            dfs(neighbor)

                start_vertex = next((v for v in adjacency_matrix if any(adjacency_matrix[v].values())), None)
                if not start_vertex:
                    return False
                dfs(start_vertex)

                return all(v in visited for v in adjacency_matrix if any(adjacency_matrix[v].values()))

            for v in adjacency_matrix:
                degree = sum(1 for neighbor in adjacency_matrix[v] if adjacency_matrix[v][neighbor] != 0)
                self.log_message(f"Vertex {v} has degree {degree}.")
                if degree % 2 != 0:
                    self.log_message(f"Vertex {v} has an odd degree. The graph is not Eulerian.")
                    return False

            if not is_connected():
                self.log_message("The graph is not connected. The graph is not Eulerian.")
                return False

            self.log_message("All vertices have an even degree and the graph is connected.")
            return True

        def hierholzer_algorithm_directed():
            self.log_message("Finding Eulerian cycle using Hierholzer's Algorithm (Directed)...")

            edges = {u: [v for v in adjacency_matrix[u] if adjacency_matrix[u][v] != 0] for u in adjacency_matrix}
            cycle = []
            stack = []
            current = next(iter(edges))

            while edges[current] or stack:
                if not edges[current]:
                    cycle.append(current)
                    current = stack.pop()
                else:
                    stack.append(current)
                    next_vertex = edges[current].pop()
                    current = next_vertex

            cycle.append(current)
            return cycle

        def hierholzer_algorithm():
            self.log_message("Finding Eulerian cycle using Hierholzer's Algorithm...")

            edges = {u: [v for v in adjacency_matrix[u] if adjacency_matrix[u][v] != 0] for u in adjacency_matrix}
            cycle = []
            stack = []
            current = next(iter(edges))

            while edges[current] or stack:
                if not edges[current]:
                    cycle.append(current)
                    current = stack.pop()
                else:
                    stack.append(current)
                    next_vertex = edges[current].pop()
                    edges[next_vertex].remove(current)
                    current = next_vertex

            cycle.append(current)
            return cycle

        if is_directed():
            if is_directed_eulerian():
                self.log_message("The directed graph is Eulerian.")
                cycle = hierholzer_algorithm_directed()
                cycle_str = " -> ".join(cycle)
                self.log_message(f"Eulerian Cycle found: {cycle_str}")
                messagebox.showinfo("Eulerian Graph", f"The directed graph is Eulerian.\nEulerian Cycle: {cycle_str}")
            else:
                self.log_message("The directed graph is not Eulerian.")
                messagebox.showerror("Not Eulerian", "The directed graph is not Eulerian.")
        else:
            eulerian = is_undirected_eulerian()
            if eulerian:
                self.log_message("The undirected graph is Eulerian.")
                cycle = hierholzer_algorithm()
                cycle_str = " -> ".join(cycle)
                self.log_message(f"Eulerian Cycle found: {cycle_str}")
                messagebox.showinfo("Eulerian Graph", f"The undirected graph is Eulerian.\nEulerian Cycle: {cycle_str}")
            else:
                self.log_message("The undirected graph is not Eulerian.")
                messagebox.showerror("Not Eulerian", "The undirected graph is not Eulerian.")

    def check_planarity(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']
        vertices = list(adjacency_matrix.keys())
        v = len(vertices)
        e = sum(len([n for n in adjacency_matrix[vertex] if adjacency_matrix[vertex][n] != 0]) for vertex in vertices) // 2

        if e > 3 * v - 6:
            self.log_message("Grafo não é planar pela fórmula de Euler.")
            messagebox.showinfo("Planarity Check", "Grafo não é planar pela fórmula de Euler.")
            return

        def contains_k5_k33(graph):
            for comb in combinations(graph.keys(), 5):
                subgraph = {v: set(n for n in graph[v] if n in comb) for v in comb}
                if all(len(neighbors) == 4 for neighbors in subgraph.values()):
                    return True

            for comb in combinations(graph.keys(), 6):
                set1, set2 = comb[:3], comb[3:]
                is_k33 = all(adjacency_matrix[v1][v2] != 0 for v1 in set1 for v2 in set2) and \
                        all(adjacency_matrix[v1][v2] == 0 for v1 in set1 for v2 in set1) and \
                        all(adjacency_matrix[v1][v2] == 0 for v1 in set2 for v2 in set2)
                if is_k33:
                    return True

            return False

        if contains_k5_k33(adjacency_matrix):
            self.log_message("Grafo contém subgrafo homeomorfo a K5 ou K3,3, então não é planar.")
            messagebox.showinfo("Planarity Check", "Grafo contém subgrafo homeomorfo a K5 ou K3,3, então não é planar.")
        else:
            self.log_message("Grafo é planar.")
            messagebox.showinfo("Planarity Check", "Grafo é planar.")

    def make_undirected(self, adjacency_matrix):
        undirected_matrix = {}
        for u in adjacency_matrix:
            undirected_matrix[u] = {}
            for v, weight in adjacency_matrix[u].items():
                if weight > 0:
                    undirected_matrix[u][v] = weight
                    if v not in undirected_matrix:
                        undirected_matrix[v] = {}
                    undirected_matrix[v][u] = weight
        return undirected_matrix

    def find_minimum_allocation(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        if not graph_info.get('has_weights', False):
            messagebox.showerror("Error", "Minimum allocation only applies to weighted, complete bipartite graphs.")
            return

        adjacency_matrix = self.make_undirected(graph_info['adjacency_matrix'])

        cost_matrix = []
        vertices = list(adjacency_matrix.keys())
        for u in vertices:
            cost_row = [adjacency_matrix[u].get(v, float('inf')) for v in vertices]
            cost_matrix.append(cost_row)

        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        min_cost = sum(cost_matrix[row][col] for row, col in zip(row_ind, col_ind))

        allocation = [f"{vertices[row]} -> {vertices[col]}" for row, col in zip(row_ind, col_ind)]
        self.log_message(f"Minimum allocation with cost {min_cost}:")
        self.log_message("\n".join(allocation))
        messagebox.showinfo("Minimum Allocation", f"Minimum allocation with cost {min_cost}:\n" + "\n".join(allocation))
        
if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()