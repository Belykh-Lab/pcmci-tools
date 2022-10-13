import networkx as nx
import numpy as np

def to_networkx(results, binarize=False, p_value=0.05):
    graph = results['graph']
    val_matrix = results['val_matrix']
    p_matrix = results['p_matrix']
    graph = graph.squeeze()

    if graph.ndim == 2:
        # If a non-time series (N,N)-graph is given, insert a dummy dimension
        graph = np.expand_dims(graph, axis = 2)
    

    N, N, dummy = graph.shape
    tau_max = dummy - 1
    max_lag = tau_max + 1


    # Define graph links by absolute maximum (positive or negative like for
    # partial correlation)
    # val_matrix[np.abs(val_matrix) < sig_thres] = 0.

    # Only draw link in one direction among contemp
    # Remove lower triangle
    link_matrix_upper = np.copy(graph)
    link_matrix_upper[:, :, 0] = np.triu(link_matrix_upper[:, :, 0])

    # net = _get_absmax(link_matrix != "")
    net = np.any(link_matrix_upper != "", axis=2)
    G = nx.DiGraph(net)

    # list of all strengths for color map
    all_strengths = []
    # Add attributes, contemporaneous and lagged links are handled separately
    for (u, v, dic) in G.edges(data=True):
        # average lagfunc for link u --> v ANDOR u -- v

        if u != v:
            for lag in range(max_lag):
                dic[f"egde_type_lag_{lag}"] = link_matrix_upper[u, v, lag]
                dic[f"edge_weight_lag_{lag}"] = val_matrix[u, v, lag]
                if binarize:
                    dic[f"binary_edge_lag_{lag}"] = p_matrix[u, v, lag] < p_value
                    dic[f"binary_edge_lag_{lag}_p_value"] = p_matrix[u, v, lag]
            all_strengths.append(dic[f"edge_weight_lag_{lag}"])
    return G, all_strengths

if __name__ == "__main__"
    H = to_networkx(results_alldata, binarize=True)
    for (u, v, dic) in H.edges(data=True):
    print(u, v, dic)
    input()
