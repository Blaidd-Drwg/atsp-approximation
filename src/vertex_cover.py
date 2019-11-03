def vertex_cover(g):
    # canonical representation for an undirected edge (u <= v)
    def edge(u, v):
        return (u, v) if u < v else (v, u)

    # finds the smallest vertex cover by building a search tree:
    # in every branch either a single node is taken into the VC, or its entire neighborhood
    def recursive_vc(g, edges_to_cover, cover):
        if not edges_to_cover:
            return set(cover)

        # pick a node
        u, v = next(iter(edges_to_cover))
        node = u if g.degree(u) > g.degree(v) else v

        # left recursion branch: take node into cover
        cover.add(node)
        covered = edges_to_cover.intersection(set(edge(node, neighbor) for neighbor in g[node]))
        edges_to_cover -= covered
        best_cover_with_node = recursive_vc(g, edges_to_cover, cover)

        # restore edges_to_cover and cover
        cover.remove(node)
        edges_to_cover |= covered

        # right recursion branch: take N(node) into cover
        neighborhood = set(g[node]) - cover
        cover |= neighborhood

        neighbor_edges = set()
        for neighbor in neighborhood:
            neighbor_edges |= set(edge(neighbor, neighbor_neighbor) for neighbor_neighbor in g[neighbor])
        covered = edges_to_cover.intersection(neighbor_edges)
        edges_to_cover -= covered
        best_cover_without_node = recursive_vc(g, edges_to_cover, cover)

        # restore edges_to_cover and cover
        cover -= neighborhood
        edges_to_cover |= covered

        return min(best_cover_with_node, best_cover_without_node, key=len)

    edges_to_cover = set(edge(u, v) for u, v in g.edges())
    cover = set()
    return recursive_vc(g, edges_to_cover, cover)
