import tkinter as tk
import subprocess
from tkinter import ttk

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Grafos")

        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        tk.Label(self.scrollable_frame, text="Escolha uma ação:").pack(pady=10)
        self.create_buttons()

    def create_buttons(self):
        actions = [
            ("1. Verificar a existência de uma dada aresta", self.check_edge),
            ("2. Informar o grau de um dado vértice", self.check_vertex_degree),
            ("3. Informar a adjacência de um dado vértice", self.check_vertex_adjacency),
            ("4. Verificar se um grafo é cíclico", self.check_if_cyclic),
            ("5. Verificar se um grafo não orientado é conexo", self.check_if_undirected_and_connected),
            ("6. Informar componentes fortemente conexos de um dígrafo", self.check_strongly_connected_components),
            ("7. Gerar uma ordenação topológica de um dígrafo acíclico", self.check_dag_and_topological_sort),
            ("8. Verificar se um grafo é euleriano", self.check_eulerian),
            ("9. Verificar se é um conjunto independente", self.check_independent_set),
            ("10. Verificar se é um clique", self.check_click),
            ("11. Verificar se é um conjunto dominante", self.check_dominating_set),
            ("12. Verificar se um grafo é planar", self.check_planarity),
            ("13. Encontrar um caminho mais curto", self.find_shortest_path),
            ("14. Encontrar um caminho de menor custo", self.find_lowest_cost_path),
            ("15. Encontrar uma árvore geradora mínima", self.find_mst),
            ("16. Verificar a alocação mínima", self.find_minimum_allocation),
        ]

        for text, command in actions:
            button = tk.Button(self.scrollable_frame, text=text, command=command)
            button.pack(pady=5, fill='x')

    def check_if_cyclic(self):
        result = subprocess.run(["python", "cyclic.py"], capture_output=True, text=True, cwd="./check")
        print(result.stdout)
        print(result.stderr)
    
    def check_dag_and_topological_sort(self):
        result = subprocess.run(["python", "dag_top_gen.py"], capture_output=True, text=True, cwd="./check")
        print(result.stdout)
        print(result.stderr)

    def check_eulerian(self):
        result = subprocess.run(["python", "eulerian.py"], capture_output=True, text=True, cwd="./check")
        print(result.stdout)
        print(result.stderr)

    def find_minimum_allocation(self):
        result = subprocess.run(["python", "min_alloc.py"], capture_output=True, text=True, cwd="./check")
        print(result.stdout)
        print(result.stderr)

    def check_planarity(self):
        result = subprocess.run(["python", "planarity.py"], capture_output=True, text=True, cwd="./check")
        print(result.stdout)
        print(result.stderr)

    def check_strongly_connected_components(self):
        result = subprocess.run(["python", "str_con_comp.py"], capture_output=True, text=True, cwd="./check")
        print(result.stdout)
        print(result.stderr)

    def check_if_undirected_and_connected(self):
        result = subprocess.run(["python", "und_con.py"], capture_output=True, text=True, cwd="./check")
        print(result.stdout)
        print(result.stderr)

    def check_click(self):
        result = subprocess.run(["python", "click.py"], capture_output=True, text=True, cwd="./gen")
        print(result.stdout)
        print(result.stderr)

    def check_dominating_set(self):
        result = subprocess.run(["python", "domain_set.py"], capture_output=True, text=True, cwd="./gen")
        print(result.stdout)
        print(result.stderr)

    def check_edge(self):
        result = subprocess.run(["python", "edge_exist.py"], capture_output=True, text=True, cwd="./gen")
        print(result.stdout)
        print(result.stderr)

    def check_independent_set(self):
        result = subprocess.run(["python", "indie_vert_set.py"], capture_output=True, text=True, cwd="./gen")
        print(result.stdout)
        print(result.stderr)

    def check_vertex_adjacency(self):
        result = subprocess.run(["python", "vert_adj.py"], capture_output=True, text=True, cwd="./gen")
        print(result.stdout)
        print(result.stderr)

    def check_vertex_degree(self):
        result = subprocess.run(["python", "vert_deg.py"], capture_output=True, text=True, cwd="./gen")
        print(result.stdout)
        print(result.stderr)

    def find_mst(self):
        result = subprocess.run(["python", "agm.py"], capture_output=True, text=True, cwd="./pathmaker")
        print(result.stdout)
        print(result.stderr)

    def find_lowest_cost_path(self):
        result = subprocess.run(["python", "least_cost.py"], capture_output=True, text=True, cwd="./pathmaker")
        print(result.stdout)
        print(result.stderr)

    def find_shortest_path(self):
        result = subprocess.run(["python", "least_path.py"], capture_output=True, text=True, cwd="./pathmaker")
        print(result.stdout)
        print(result.stderr)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = MainApp(root)
    root.mainloop()