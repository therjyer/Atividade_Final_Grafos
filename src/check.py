import tkinter as tk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificador de Grafos")

        tk.Label(self.root, text="Escolha uma ação:").pack(pady=10)

        tk.Button(self.root, text="Verificar se o Grafo é Cíclico", command=self.check_if_cyclic).pack(pady=10)
        tk.Button(self.root, text="Gerar uma Ordenação Topológica em um DAG", command=self.check_dag_and_topological_sort).pack(pady=10)
        tk.Button(self.root, text="Verificar se o Grafo é Euleriano", command=self.check_eulerian).pack(pady=10)
        tk.Button(self.root, text="Encontrar Alocação Mínima", command=self.find_minimum_allocation).pack(pady=10)
        tk.Button(self.root, text="Verificar Planaridade", command=self.check_planarity).pack(pady=10)
        tk.Button(self.root, text="Verificar Componentes Fortemente Conectados", command=self.check_strongly_connected_components).pack(pady=10)
        tk.Button(self.root, text="Verificar se o Grafo é Não Direcionado e Conectado", command=self.check_if_undirected_and_connected).pack(pady=10)

    def check_if_cyclic(self):
        result = subprocess.run(["python", "cyclic.py"], capture_output=True, text=True, cwd="../check")
        print(result.stdout)
        print(result.stderr)
    
    def check_dag_and_topological_sort(self):
        result = subprocess.run(["python", "dag_top_gen.py"], capture_output=True, text=True, cwd="../check")
        print(result.stdout)
        print(result.stderr)
    
    def check_eulerian(self):
        result = subprocess.run(["python", "eulerian.py"], capture_output=True, text=True, cwd="../check")
        print(result.stdout)
        print(result.stderr)
    
    def find_minimum_allocation(self):
        result = subprocess.run(["python", "min_alloc.py"], capture_output=True, text=True, cwd="../check")
        print(result.stdout)
        print(result.stderr)
    
    def check_planarity(self):
        result = subprocess.run(["python", "planarity.py"], capture_output=True, text=True, cwd="../check")
        print(result.stdout)
        print(result.stderr)
    
    def check_strongly_connected_components(self):
        result = subprocess.run(["python", "str_con_comp.py"], capture_output=True, text=True, cwd="../check")
        print(result.stdout)
        print(result.stderr)
    
    def check_if_undirected_and_connected(self):
        result = subprocess.run(["python", "und_con.py"], capture_output=True, text=True, cwd="../check")
        print(result.stdout)
        print(result.stderr)
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = MainApp(root)
    root.mainloop()