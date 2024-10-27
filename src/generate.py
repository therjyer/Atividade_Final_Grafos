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
        tk.Button(self.root, text="Check Vertex Degree", command=self.check_vertex_degree).pack()
        tk.Button(self.root, text="Check Vertex Adjacency", command=self.check_vertex_adjacency).pack()

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


if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()