import tkinter as tk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de itens em Grafos")

        tk.Label(self.root, text="Escolha uma ação:").pack(pady=10)
       
        tk.Button(self.root, text="Verificar Clique", command=self.check_click).pack(pady=10)
        tk.Button(self.root, text="Verificar Conjunto Dominante", command=self.check_dominating_set).pack(pady=10)
        tk.Button(self.root, text="Verificar Existência de Aresta", command=self.check_edge).pack(pady=10)
        tk.Button(self.root, text="Verificar Conjunto de Vértices Independentes", command=self.check_independent_set).pack(pady=10)
        tk.Button(self.root, text="Verificar Adjacência do Vértice", command=self.check_vertex_adjacency).pack(pady=10)
        tk.Button(self.root, text="Verificar Grau do Vértice", command=self.check_vertex_degree).pack(pady=10)
        

    def check_click(self):
        result = subprocess.run(["python", "click.py"], capture_output=True, text=True, cwd="../gen")
        print(result.stdout)
        print(result.stderr)
    
    def check_dominating_set(self):
        result = subprocess.run(["python", "domain_set.py"], capture_output=True, text=True, cwd="../gen")
        print(result.stdout)
        print(result.stderr)
    
    def check_edge(self):
        result = subprocess.run(["python", "edge_exist.py"], capture_output=True, text=True, cwd="../gen")
        print(result.stdout)
        print(result.stderr)
    
    def check_independent_set(self):
        result = subprocess.run(["python", "indie_vert_set.py"], capture_output=True, text=True, cwd="../gen")
        print(result.stdout)
        print(result.stderr)
    
    def check_vertex_adjacency(self):
        result = subprocess.run(["python", "vert_adj.py"], capture_output=True, text=True, cwd="../gen")
        print(result.stdout)
        print(result.stderr)
    
    def check_vertex_degree(self):
        result = subprocess.run(["python", "vert_deg.py"], capture_output=True, text=True, cwd="../gen")
        print(result.stdout)
        print(result.stderr)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = MainApp(root)
    root.mainloop()