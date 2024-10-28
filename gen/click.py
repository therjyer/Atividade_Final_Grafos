import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class VerificationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Verificações de Grafos")
        self.graph_data = {}
        self.graph_names = []
        self.load_graphs()
        self.create_widgets()

    def load_graphs(self):
        if not os.path.exists("../lib/adjacency_matrix.json"):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            self.root.destroy()
            return
        with open("../lib/adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        self.graph_names = list(self.graph_data.keys())

    def create_widgets(self):
        tk.Label(self.root, text="Selecione um grafo para verificação:").pack()
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, *self.graph_names)
        self.graph_menu.pack()
        
        self.log_text = tk.Text(self.root, height=20, width=70)
        self.log_text.pack()
        
        tk.Button(self.root, text="Verificar Clique", command=self.check_click).pack(pady=20)

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            return None
        return self.graph_data[graph_name]

    def check_click(self):
        self.log_text.delete(1.0, tk.END)
        self.log_message("Iniciando verificação de clique...")

        graph_info = self.get_selected_graph()
        if not graph_info:
            return

        adjacency_matrix = graph_info['adjacency_matrix']

        vertices_input = simpledialog.askstring("Entrada", "Digite o conjunto de vértices (separados por vírgula):")
        if not vertices_input:
            self.log_message("Nenhum vértice fornecido.")
            return

        vertices = vertices_input.split(',')
        vertices = [v.strip() for v in vertices]

        self.log_message(f"Vértices fornecidos: {vertices}")

        for i, v1 in enumerate(vertices):
            if v1 not in adjacency_matrix:
                self.log_message(f"Vértice {v1} não existe no grafo.")
                messagebox.showerror("Não é um Clique", f"Vértice {v1} não existe no grafo.")
                return
            for v2 in vertices[i+1:]:
                if v2 not in adjacency_matrix:
                    self.log_message(f"Vértice {v2} não existe no grafo.")
                    messagebox.showerror("Não é um Clique", f"Vértice {v2} não existe no grafo.")
                    return
                
                if adjacency_matrix[v1].get(v2, 1) == 0:
                    self.log_message(f"Vértices {v1} e {v2} não são adjacentes. O conjunto não é um clique.")
                    messagebox.showerror("Não é um Clique", f"Vértices {v1} e {v2} não são adjacentes. O conjunto não é um clique.")
                    return

        self.log_message("O conjunto é um clique.")
        messagebox.showinfo("Clique", "O conjunto é um clique.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    app = VerificationApp(root)
    root.mainloop()