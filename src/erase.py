import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class EraseGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Erase Graph")

        self.graph_data = {}
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
        tk.Label(self.root, text="Select a graph to delete:").pack()
        
        self.selected_graph = tk.StringVar(value="Choose a graph")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()

        tk.Button(self.root, text="Delete Graph", command=self.delete_graph).pack()

    def delete_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Choose a graph" or graph_name not in self.graph_data:
            messagebox.showerror("Error", "Please select a valid graph to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the graph '{graph_name}'?")
        if confirm:
            del self.graph_data[graph_name]
            self.save_changes()
            messagebox.showinfo("Deleted", f"Graph '{graph_name}' has been deleted.")

    def save_changes(self):
        with open("adjacency_matrix.json", "w") as f:
            json.dump(self.graph_data, f, indent=4)
        messagebox.showinfo("Saved", "Changes saved to adjacency_matrix.json")

if __name__ == "__main__":
    root = tk.Tk()
    app = EraseGraphApp(root)
    root.mainloop()