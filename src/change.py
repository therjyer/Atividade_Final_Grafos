import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class ChangeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Edit Existing Graphs")
        
        self.graph_data = {}
        self.graph_name = None
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
        tk.Label(self.root, text="Select a graph to edit:").pack()
        
        self.selected_graph = tk.StringVar(value="Choose a graph")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()

        tk.Button(self.root, text="Rename Graph", command=self.rename_graph).pack()
        tk.Button(self.root, text="Change Graph Type", command=self.change_graph_type).pack()
        tk.Button(self.root, text="Add/Remove Vertex", command=self.modify_vertices).pack()
        tk.Button(self.root, text="Rename Vertex", command=self.rename_vertex).pack()
        tk.Button(self.root, text="Change Edge Vertices", command=self.change_edge_vertices).pack()
        tk.Button(self.root, text="Change Edge Weight", command=self.change_edge_weight).pack()

    def get_graph_info(self):
        self.graph_name = self.selected_graph.get()
        if self.graph_name == "Choose a graph" or self.graph_name not in self.graph_data:
            messagebox.showerror("Error", "Please select a valid graph.")
            return None
        return self.graph_data[self.graph_name]

    def save_changes(self):
        with open("../lib/adjacency_matrix.json", "w") as f:
            json.dump(self.graph_data, f, indent=4)
        messagebox.showinfo("Saved", f"Changes saved to adjacency_matrix.json")

    def rename_graph(self):
        self.graph_name = self.selected_graph.get()
        if self.graph_name == "Choose a graph" or self.graph_name not in self.graph_data:
            messagebox.showerror("Error", "Please select a valid graph to rename.")
            return

        new_name = simpledialog.askstring("Rename Graph", "Enter a new name for the graph:")
        if new_name:
            if new_name in self.graph_data:
                messagebox.showerror("Error", "A graph with that name already exists.")
                return
            self.graph_data[new_name] = self.graph_data.pop(self.graph_name)
            self.graph_name = new_name
            self.selected_graph.set(new_name)
            self.save_changes()

    def change_graph_type(self):
        graph_info = self.get_graph_info()
        if graph_info:
            new_type = "undirected" if graph_info["type"] == "directed" else "directed"
            graph_info["type"] = new_type
            self.save_changes()

    def modify_vertices(self):
        graph_info = self.get_graph_info()
        if graph_info:
            choice = messagebox.askyesno("Modify Vertices", "Would you like to add a vertex?")
            if choice:
                new_vertex = simpledialog.askstring("Add Vertex", "Enter the new vertex name:")
                if new_vertex and new_vertex not in graph_info["adjacency_matrix"]:
                    graph_info["adjacency_matrix"][new_vertex] = {v: 0 for v in graph_info["adjacency_matrix"]}
                    for v in graph_info["adjacency_matrix"]:
                        graph_info["adjacency_matrix"][v][new_vertex] = 0
            else:
                remove_vertex = simpledialog.askstring("Remove Vertex", "Enter the name of the vertex to remove:")
                if remove_vertex and remove_vertex in graph_info["adjacency_matrix"]:
                    del graph_info["adjacency_matrix"][remove_vertex]
                    for v in graph_info["adjacency_matrix"]:
                        if remove_vertex in graph_info["adjacency_matrix"][v]:
                            del graph_info["adjacency_matrix"][v][remove_vertex]
            self.save_changes()

    def rename_vertex(self):
        graph_info = self.get_graph_info()
        if graph_info:
            old_vertex = simpledialog.askstring("Rename Vertex", "Enter the name of the vertex to rename:")
            if old_vertex and old_vertex in graph_info["adjacency_matrix"]:
                new_vertex = simpledialog.askstring("New Vertex Name", "Enter the new name for the vertex:")
                if new_vertex and new_vertex not in graph_info["adjacency_matrix"]:
                    graph_info["adjacency_matrix"][new_vertex] = graph_info["adjacency_matrix"].pop(old_vertex)
                    for v in graph_info["adjacency_matrix"]:
                        if old_vertex in graph_info["adjacency_matrix"][v]:
                            graph_info["adjacency_matrix"][v][new_vertex] = graph_info["adjacency_matrix"][v].pop(old_vertex)
                    self.save_changes()
                else:
                    messagebox.showerror("Error", "New vertex name already exists or is invalid.")
            else:
                messagebox.showerror("Error", "Vertex not found.")

    def change_edge_vertices(self):
        graph_info = self.get_graph_info()
        if graph_info:
            old_edge = simpledialog.askstring("Change Edge", "Enter the edge (e.g., A-B):")
            if old_edge:
                v1, v2 = old_edge.split("-")
                if v1 in graph_info["adjacency_matrix"] and v2 in graph_info["adjacency_matrix"][v1]:
                    new_v1 = simpledialog.askstring("New Origin", "Enter the new origin vertex:")
                    new_v2 = simpledialog.askstring("New Destination", "Enter the new destination vertex:")
                    if new_v1 and new_v2:
                        weight = graph_info["adjacency_matrix"][v1].pop(v2)
                        if v1 in graph_info["adjacency_matrix"] and new_v1 in graph_info["adjacency_matrix"]:
                            graph_info["adjacency_matrix"][new_v1][new_v2] = weight
            self.save_changes()

    def change_edge_weight(self):
        graph_info = self.get_graph_info()
        if graph_info:
            edge = simpledialog.askstring("Change Edge Weight", "Enter the edge (e.g., A-B):")
            if edge:
                v1, v2 = edge.split("-")
                if v1 in graph_info["adjacency_matrix"] and v2 in graph_info["adjacency_matrix"][v1]:
                    new_weight = simpledialog.askinteger("New Weight", f"Enter the new weight for edge {v1}-{v2}:")
                    if new_weight is not None:
                        graph_info["adjacency_matrix"][v1][v2] = new_weight
                        if graph_info["type"] == "undirected":
                            graph_info["adjacency_matrix"][v2][v1] = new_weight
            self.save_changes()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChangeGraphApp(root)
    root.mainloop()