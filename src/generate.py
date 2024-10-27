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
        
        tk.Button(self.root, text="Check Vertex Degree", command=self.check_vertex_degree).pack()
        tk.Button(self.root, text="Check Vertex Adjacency", command=self.check_vertex_adjacency).pack()
        tk.Button(self.root, text="Check Independent Vertex Set", command=self.check_independent_set).pack()
        tk.Button(self.root, text="Check Clique", command=self.check_clique).pack()
        tk.Button(self.root, text="Check Dominating Set", command=self.check_dominating_set).pack()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Choose a graph" or graph_name not in self.graph_data:
            messagebox.showerror("Error", "Please select a valid graph name.")
            return None
        return self.graph_data[graph_name]

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

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()