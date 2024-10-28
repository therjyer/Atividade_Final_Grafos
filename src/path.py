import tkinter as tk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de itens em Grafos")

        tk.Label(self.root, text="Escolha uma ação:").pack(pady=10)

        tk.Button(self.root, text="Encontrar Árvore Geradora Mínima", command=self.find_mst).pack(pady=10)
        tk.Button(self.root, text="Encontrar Caminho de Menor Custo", command=self.find_lowest_cost_path).pack(pady=10)
        tk.Button(self.root, text="Encontrar Caminho Mais Curto", command=self.find_shortest_path).pack(pady=10)

    def find_mst(self):
        result = subprocess.run(["python", "agm.py"], capture_output=True, text=True, cwd="../pathmaker")
        print(result.stdout)
        print(result.stderr)
    
    def find_lowest_cost_path(self):
        result = subprocess.run(["python", "least_cost.py"], capture_output=True, text=True, cwd="../pathmaker")
        print(result.stdout)
        print(result.stderr)
    
    def find_shortest_path(self):
        result = subprocess.run(["python", "least_path.py"], capture_output=True, text=True, cwd="../pathmaker")
        print(result.stdout)
        print(result.stderr)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = MainApp(root)
    root.mainloop()