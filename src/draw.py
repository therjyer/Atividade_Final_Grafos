import json
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def draw_graph_from_json(file_path, graph_name):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if graph_name not in data:
        print(f"Grafo '{graph_name}' não encontrado.")
        return

    graph_data = data[graph_name]

    G = nx.DiGraph() if graph_data["type"] == "directed" else nx.Graph()

    for node, edges in graph_data["adjacency_matrix"].items():
        for target, weight in edges.items():
            if weight > 0:
                G.add_edge(node, target, weight=weight)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=16, font_weight='bold')
    
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title(graph_name)
    plt.show()

def create_graph_buttons(frame, graph_names):
    for graph_name in graph_names:
        button = tk.Button(frame, text=graph_name, command=lambda name=graph_name: draw_graph_from_json('../lib/adjacency_matrix.json', name))
        button.pack(pady=10, fill='x')

root = tk.Tk()
root.title("Seleção de Grafo")
root.geometry("640x480") 

canvas = tk.Canvas(root)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

with open('../lib/adjacency_matrix.json', 'r') as file:
    data = json.load(file)

graph_names = list(data.keys())

create_graph_buttons(scrollable_frame, graph_names)

root.mainloop()