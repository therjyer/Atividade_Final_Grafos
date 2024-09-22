class Grafo:
    def __init__(self, orientado=False):
        self.orientado = orientado
        self.vertices = []
        self.arestas = []
        self.adjacencia = {}

    def inserir_grafo(self):
        num_vertices = int(input("Quantos vértices o grafo possui? "))
        self.vertices = [i for i in range(num_vertices)]
        self.adjacencia = {v: [] for v in self.vertices}

        num_arestas = int(input("Quantas arestas o grafo possui? "))
        for _ in range(num_arestas):
            u = int(input("Vértice de origem: "))
            v = int(input("Vértice de destino: "))
            if self.orientado:
                peso = int(input(f"Peso da aresta ({u} -> {v}): ") or 1)
                self.arestas.append((u, v, peso))
                self.adjacencia[u].append((v, peso))
            else:
                peso = int(input(f"Peso da aresta ({u} -- {v}): ") or 1)
                self.arestas.append((u, v, peso))
                self.adjacencia[u].append((v, peso))
                self.adjacencia[v].append((u, peso))

    def existe_aresta(self, u, v):
        return any(vertice == v for vertice, _ in self.adjacencia[u])

    def grau_vertice(self, v):
        if self.orientado:
            grau_entrada = sum(1 for u in self.adjacencia if any(v == w for w, _ in self.adjacencia[u]))
            grau_saida = len(self.adjacencia[v])
            return grau_entrada, grau_saida
        else:
            return len(self.adjacencia[v])

    def adjacencia_vertice(self, v):
        return [u for u, _ in self.adjacencia[v]]

    def grafo_ciclico(self):
        visitado = {v: False for v in self.vertices}
        def dfs(v, parent):
            visitado[v] = True
            for u, _ in self.adjacencia[v]:
                if not visitado[u]:
                    if dfs(u, v):
                        return True
                elif parent != u:
                    return True
            return False

        for v in self.vertices:
            if not visitado[v]:
                if dfs(v, -1):
                    return True
        return False

    def grafo_conexo(self):
        visitado = {v: False for v in self.vertices}
        fila = [self.vertices[0]]
        visitado[self.vertices[0]] = True

        while fila:
            v = fila.pop(0)
            for u, _ in self.adjacencia[v]:
                if not visitado[u]:
                    visitado[u] = True
                    fila.append(u)

        return all(visitado.values())

orientado = input("O grafo é orientado? (s/n): ").strip().lower() == 's'
grafo = Grafo(orientado)
grafo.inserir_grafo()

u = int(input("Digite o vértice de origem para verificar a aresta: "))
v = int(input("Digite o vértice de destino para verificar a aresta: "))
print(f"Existe aresta entre {u} e {v}?", grafo.existe_aresta(u, v))

vertice = int(input("Digite um vértice para verificar o grau: "))
if orientado:
    grau_entrada, grau_saida = grafo.grau_vertice(vertice)
    print(f"Grau de entrada: {grau_entrada}, Grau de saída: {grau_saida}")
else:
    print(f"Grau do vértice {vertice}: {grafo.grau_vertice(vertice)}")

vertice_adjacente = int(input("Digite um vértice para verificar a adjacência: "))
print(f"Adjacência do vértice {vertice_adjacente}: {grafo.adjacencia_vertice(vertice_adjacente)}")

print("Grafo é cíclico?", grafo.grafo_ciclico())
print("Grafo é conexo?", grafo.grafo_conexo())