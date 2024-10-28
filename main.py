import tkinter as tk
import subprocess

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Grafos")

        tk.Label(self.root, text="Escolha uma ação:").pack(pady=10)

        tk.Button(self.root, text="Criar Novo Grafo", command=self.create_graph).pack(pady=10)
        tk.Button(self.root, text="Editar Grafo Existente", command=self.edit_graph).pack(pady=10)
        tk.Button(self.root, text="Visualizar Grafo", command=self.visualize_graph).pack(pady=10)
        tk.Button(self.root, text="Deletar Grafo", command=self.delete_graph).pack(pady=10)
        tk.Button(self.root, text="Fazer verificações", command=self.check_graph).pack(pady=10)
        tk.Button(self.root, text="Fazer perguntas", command=self.quest_graph).pack(pady=10)
        tk.Button(self.root, text="Geradores", command=self.gen_graph).pack(pady=10)

    def create_graph(self):
        result = subprocess.run(["python", "create.py"], capture_output=True, text=True, cwd="./src")
        print(result.stdout)
        print(result.stderr)

    def edit_graph(self):
        result = subprocess.run(["python", "change.py"], capture_output=True, text=True, cwd="./src")
        print(result.stdout)
        print(result.stderr)
    
    def visualize_graph(self):
        result = subprocess.run(["python", "draw.py"], capture_output=True, text=True, cwd="./src")
        print(result.stdout)
        print(result.stderr)

    def delete_graph(self):
        result = subprocess.run(["python", "erase.py"], capture_output=True, text=True, cwd="./src")
        print(result.stdout)
        print(result.stderr)
    
    def check_graph(self):
        result = subprocess.run(["python", "check.py"], capture_output=True, text=True, cwd="./src")
        print(result.stdout)
        print(result.stderr)
    
    def quest_graph(self):
        result = subprocess.run(["python", "quest.py"], capture_output=True, text=True, cwd="./src")
        print(result.stdout)
        print(result.stderr)
    
    def gen_graph(self):
        result = subprocess.run(["python", "path.py"], capture_output=True, text=True, cwd="./src")
        print(result.stdout)
        print(result.stderr)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = MainApp(root)
    root.mainloop()