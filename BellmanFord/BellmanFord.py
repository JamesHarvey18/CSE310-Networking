graph_edges = [[0, 1, 9], [0, 3, 14], [0, 4, 15], [1, 2, 24], [2, 5, 2], [2, 7, 19], [3, 2, 18], [3, 5, 30],
               [3, 4, 5], [4, 5, 20], [4, 7, 44], [5, 7, 16 ], [5, 6, 11], [6, 2, 6], [6, 7, 6]]
vertex_translation = {0: 'x', 1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'e', 7: 'y'}
parent = []
source = 0
final_destination = 7

def BellmanFord():

    current_paths = []

    for i in range(final_destination + 1):
        current_paths.append(float("inf"))
        parent.append(0)

    current_paths[0] = 0
    parent[0] = 0

    for i in range(final_destination):
        for src, dst, weight in graph_edges:
            if current_paths[src] != float("inf") and current_paths[src] + weight < current_paths[dst]:
                current_paths[dst] = current_paths[src] + weight
                parent[dst] = src

    print("Minimum Cost from X to Y: ", current_paths[7])


def shortest_path(vertex):
    if parent[vertex] == 0:
        print("x->", vertex_translation[vertex])
        return
    shortest_path(parent[vertex])
    print("->", vertex_translation[vertex])


BellmanFord()
shortest_path(final_destination)
