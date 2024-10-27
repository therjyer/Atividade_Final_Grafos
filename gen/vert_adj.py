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
        
        # Criação do widget de log imediatamente
        self.log_text = tk.Text(self.root, height=15, width=50)
        self.log_text.pack()

        self.log_message("Inicializando o aplicativo...")
        self.create_widgets()  # Criar widgets que não dependem de grafos
        self.load_graphs()
        self.log_message("Aplicativo inicializado.")

    def load_graphs(self):
        self.log_message("Tentando carregar grafos do arquivo...")
        if not os.path.exists("../lib/adjacency_matrix.json"):
            messagebox.showerror("Erro", "Arquivo não encontrado.")
            self.log_message("Erro: Arquivo não encontrado.")
            self.root.destroy()
            return
        with open("../lib/adjacency_matrix.json", "r") as f:
            self.graph_data = json.load(f)
        self.graph_names = list(self.graph_data.keys())
        self.log_message(f"{len(self.graph_names)} grafos carregados com sucesso.")
        
        # Atualiza o OptionMenu após carregar os grafos
        self.update_graph_menu()

    def create_widgets(self):
        self.log_message("Criando widgets da interface...")
        tk.Label(self.root, text="Selecione um grafo para verificação:").pack()
        
        self.selected_graph = tk.StringVar(value="Escolha um grafo")
        
        # Criar o OptionMenu sem opções inicialmente
        self.graph_menu = tk.OptionMenu(self.root, self.selected_graph, "")
        self.graph_menu.pack()

        tk.Button(self.root, text="Verificar Adjacência do Vértice", command=self.check_vertex_adjacency).pack()
        self.log_message("Widgets criados.")

    def update_graph_menu(self):
        # Atualiza as opções do OptionMenu com os grafos carregados
        menu = self.graph_menu['menu']
        menu.delete(0, 'end')  # Limpa opções existentes
        for name in self.graph_names:
            menu.add_command(label=name, command=lambda value=name: self.selected_graph.set(value))
        self.selected_graph.set("Escolha um grafo")  # Define valor padrão

    def log_message(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def get_selected_graph(self):
        graph_name = self.selected_graph.get()
        if graph_name == "Escolha um grafo" or graph_name not in self.graph_data:
            messagebox.showerror("Erro", "Por favor, selecione um nome de grafo válido.")
            self.log_message("Erro: Nome de grafo inválido selecionado.")
            return None
        self.log_message(f"Grafo selecionado: {graph_name}.")
        return self.graph_data[graph_name]

    def check_vertex_adjacency(self):
        graph_info = self.get_selected_graph()
        if not graph_info:
            self.log_message("Verificação de adjacência cancelada.")
            return

        vertex = simpledialog.askstring("Vértice", "Digite o vértice para verificar a adjacência:")
        self.log_message(f"Vértice solicitado: {vertex}.")

        if vertex:
            adjacency_matrix = graph_info['adjacency_matrix']
            if vertex in adjacency_matrix:
                adjacent_vertices = [v for v in adjacency_matrix[vertex] if adjacency_matrix[vertex][v] != 0]
                if adjacent_vertices:
                    messagebox.showinfo("Adjacência do Vértice", f"Vértices adjacentes a {vertex}: {', '.join(adjacent_vertices)}.")
                    self.log_message(f"Vértices adjacentes a {vertex}: {', '.join(adjacent_vertices)}.")
                else:
                    messagebox.showinfo("Adjacência do Vértice", f"O vértice {vertex} não possui vértices adjacentes.")
                    self.log_message(f"O vértice {vertex} não possui vértices adjacentes.")
            else:
                messagebox.showerror("Erro", f"O vértice {vertex} não existe no grafo.")
                self.log_message(f"Erro: O vértice {vertex} não existe no grafo.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VerificationApp(root)
    root.mainloop()