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

def on_select(event):
    selected_graph = graph_var.get()
    draw_graph_from_json('adjacency_matrix.json', selected_graph)

root = tk.Tk()
root.title("Seleção de Grafo")

with open('adjacency_matrix.json', 'r') as file:
    data = json.load(file)

graph_names = list(data.keys())

graph_var = tk.StringVar(value=graph_names[0])  # Valor inicial

option_menu = ttk.OptionMenu(root, graph_var, graph_var.get(), *graph_names, command=on_select)
option_menu.pack(pady=20)

root.mainloop()
