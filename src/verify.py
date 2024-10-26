import tkinter as tk
from tkinter import messagebox, simpledialog
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
        
        tk.Button(self.root, text="Check Edge Existence", command=self.check_edge).pack()
        tk.Button(self.root, text="Check if Graph is Cyclic", command=self.check_if_cyclic).pack()
        tk.Button(self.root, text="Check if Graph is Undirected and Connected", command=self.check_if_undirected_and_connected).pack()
        tk.Button(self.root, text="Check Strongly Connected Components", command=self.check_strongly_connected_components).pack()
        tk.Button(self.root, text="Generate a Topological Sort in a DAG", command=self.check_dag_and_topological_sort).pack()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()