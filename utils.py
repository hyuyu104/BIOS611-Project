import numpy as np
import pyreadr
from matplotlib import pyplot as plt
from scipy.spatial.distance import pdist

plt.style.use("seaborn-v0_8-paper")
plt.rcParams.update({
    "figure.constrained_layout.use": True,
    "font.size": 10,
    "font.weight": "bold",
    # remove top and right spines
    "axes.spines.right": False,
    "axes.spines.top": False,
    # remove the border of legend
    "legend.frameon": False,
    "legend.loc": (1, 0.5)
})


def prepare_data(path="data/Layer2_BC_Count.rds"):
    data = pyreadr.read_r(path)["rawcount"].T
    locations = np.stack(data.index.str.split("x")).astype("float64").T
    data["x"] = locations[0]
    data["y"] = locations[1]
    data = data.set_index(["x", "y"])
    return data


def normalize_data(data):
    gene_std = data.std().sort_values(ascending=False)
    low_var = data[gene_std.index[gene_std < 5]]
    
    means = low_var.mean(axis=1).to_frame("a").values
    data_norm = data/means
    return gene_std, data_norm


def gpca(X, locs, l, k, n):
    pdist_mat = np.zeros((X.shape[0], X.shape[0]))
    pdist_arr = pdist(locs)
    pdist_mat[np.triu_indices_from(pdist_mat, 1)] = pdist_arr
    pdist_mat = pdist_mat + pdist_mat.T
    # generate rank for each row
    ranks = pdist_mat.argsort(axis=0).argsort(axis=0)
    A = (ranks <= k).astype("int64")
    A = ((A + A.T)/2 > 0).astype("int64")
    np.fill_diagonal(A, 0)
    D = np.diag(np.sum(A, axis=1))

    L = D - A
    K = np.linalg.inv(np.identity(L.shape[0]) - l*L)
    Vk = np.linalg.eigh(X.T@K@X)[1][:,-n:]
    return K@X@Vk