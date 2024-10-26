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
        cycle_count = 0
        cycle_vertices = set()

        def has_cycle(v, visited, parent, path):
            visited.add(v)
            path.add(v)
            for neighbor in adjacency_matrix[v]:
                if adjacency_matrix[v][neighbor] != 0:
                    if neighbor not in visited:
                        if has_cycle(neighbor, visited, v, path):
                            return True
                    elif parent != neighbor:
                        cycle_vertices.update(path)
                        return True
            path.remove(v)
            return False

        for vertex in vertices:
            if vertex not in visited:
                path = set()
                if has_cycle(vertex, visited, None, path):
                    cycle_count += 1

        total_vertices = len(vertices)

        if cycle_count > 0:
            messagebox.showinfo("Graph Cyclic Check", 
                f"The graph contains {cycle_count} cycle(s).\n"
                f"Total vertices: {total_vertices}\n"
                f"Vertices involved in cycle(s): {', '.join(cycle_vertices)}.")
        else:
            messagebox.showinfo("Graph Cyclic Check", 
                f"The graph does not contain a cycle.\nTotal vertices: {total_vertices}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()