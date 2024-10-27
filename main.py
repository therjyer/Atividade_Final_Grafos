import tkinter as tk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Manager")

        tk.Label(self.root, text="Choose an action:").pack(pady=10)

        tk.Button(self.root, text="Create New Graph", command=self.create_graph).pack(pady=5)
        tk.Button(self.root, text="Edit Existing Graph", command=self.edit_graph).pack(pady=5)
        tk.Button(self.root, text="Visualize Graph", command=self.visualize_graph).pack(pady=5)
        tk.Button(self.root, text="Delete Graph", command=self.delete_graph).pack(pady=5)
        tk.Button(self.root, text="Make verifications", command=self.check_graph).pack(pady=5)
        tk.Button(self.root, text="Do questions", command=self.generate_graph).pack(pady=5)

    def create_graph(self):
        subprocess.run(["python", "./src/graph.py"])

    def edit_graph(self):
        subprocess.run(["python", "./src/change.py"])

    def visualize_graph(self):
        subprocess.run(["python", "./src/draw.py"])

    def delete_graph(self):
        subprocess.run(["python", "./src/erase.py"])
    
    def check_graph(self):
        subprocess.run(["python", "./src/check.py"])
    
    def generate_graph(self):
        subprocess.run(["python", "./src/generate.py"])

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
