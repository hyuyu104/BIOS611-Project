import os
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

from utils import prepare_data, normalize_data, gpca


def fig6(data, gene_std, data_norm):
    high_var = data_norm[gene_std.index[gene_std > 5]].values
    X = high_var - high_var.mean(axis=0)

    n = 10

    fig, axes = plt.subplots(1, 2, figsize=(8, 2.5))
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    trf_arr = U[:,:n]@np.diag(S[:n])
    kmeans = KMeans(4, random_state=0).fit(trf_arr)
    clus_df = pd.DataFrame(
        kmeans.labels_, index=data.index, columns=["Cluster"]
    ).reset_index()
    axes[0].hexbin(x=clus_df.x, y=clus_df.y, C=clus_df.Cluster, gridsize=15)
    sns.scatterplot(clus_df, x="x", y="y", hue="Cluster", palette="viridis", edgecolor="grey", ax=axes[0])
    axes[0].set(xticks=[], yticks=[], title=f"PCA", xlabel="", ylabel="")
    axes[0].spines[["left", "bottom"]].set_visible(False)

    locs = np.stack(data_norm.index.values)
    Z = gpca(X, locs, 3, 5, n)
    kmeans = KMeans(4, random_state=0).fit(Z)
    clus_df = pd.DataFrame(
        kmeans.labels_, index=data.index, columns=["Cluster"]
    ).reset_index()
    axes[1].hexbin(x=clus_df.x, y=clus_df.y, C=clus_df.Cluster, gridsize=15)
    sns.scatterplot(clus_df, x="x", y="y", hue="Cluster", palette="viridis", edgecolor="grey", axes=axes[1])
    axes[1].set(xticks=[], yticks=[], title=f"GraphPCA", xlabel="", ylabel="")
    axes[1].spines[["left", "bottom"]].set_visible(False)

    fig.savefig(os.path.join("output", "3pca_gpca_compare.pdf"), bbox_inches="tight")
    
    
def fig7(data, gene_std, data_norm):
    high_var = data_norm[gene_std.index[gene_std > 5]].values
    X = high_var - high_var.mean(axis=0)

    n = 10
    locs = np.stack(data_norm.index.values)

    ls = [0, 3, 5, 10, 50]
    ks = [1, 3, 5, 10]

    fig, axes = plt.subplots(len(ks), len(ls), figsize=(12, 8))
    for i, k in enumerate(ks):
        for j, l in enumerate(ls):
            Z = gpca(X, locs, l, k, n)
            kmeans = KMeans(4, random_state=0).fit(Z)
            clus_df = pd.DataFrame(
                kmeans.labels_, index=data.index, columns=["Cluster"]
            ).reset_index()
            
            ax = axes[i][j]
            ax.hexbin(x=clus_df.x, y=clus_df.y, C=clus_df.Cluster, gridsize=15)
            sns.scatterplot(clus_df, x="x", y="y", hue="Cluster", palette="viridis", edgecolor="grey", ax=ax)
            ax.get_legend().set_visible(False)
            ax.set(xticks=[], yticks=[], title=f"l = {l}, k = {k}", xlabel="", ylabel="")
            ax.spines[["left", "bottom"]].set_visible(False)
            
    fig.savefig(os.path.join("output", "3gpca_params.pdf"), bbox_inches="tight")
    
    
if __name__ == "__main__":
    data = prepare_data()
    gene_std, data_norm = normalize_data(data)
    fig6(data, gene_std, data_norm)
    fig7(data, gene_std, data_norm)