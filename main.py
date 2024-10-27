import tkinter as tk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Grafos")

        tk.Label(self.root, text="Escolha uma ação:").pack(pady=10)

        tk.Button(self.root, text="Criar Novo Grafo", command=self.create_graph).pack(pady=5)
        tk.Button(self.root, text="Editar Grafo Existente", command=self.edit_graph).pack(pady=5)
        tk.Button(self.root, text="Visualizar Grafo", command=self.visualize_graph).pack(pady=5)
        tk.Button(self.root, text="Deletar Grafo", command=self.delete_graph).pack(pady=5)
        tk.Button(self.root, text="Fazer verificações", command=self.check_graph).pack(pady=5)
        tk.Button(self.root, text="Fazer perguntas", command=self.generate_graph).pack(pady=5)

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
