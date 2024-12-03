import os
import seaborn as sns
from matplotlib import pyplot as plt

from utils import prepare_data, normalize_data


def fig3(data):
    y = "Mean mRNA"
    gene_std = data.std().sort_values(ascending=False)
    low_var = data[gene_std.index[gene_std < 5]]
    df = low_var.mean(axis=1).to_frame(y).reset_index()
    
    fig = plt.figure(figsize=(10, 3.5))
    
    ax1 = fig.add_subplot(1, 2, 1)
    sns.scatterplot(df, x="x", y="y", hue=y, palette="Reds", ax=ax1)
    ax1.set(xticks=[], yticks=[])
    ax1.spines[["left", "bottom"]].set_visible(False)
    
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.scatter(df.x, df.y, df["Mean mRNA"], c=df["Mean mRNA"])
    ax2.set(xlabel="x", ylabel="y")
    
    fig.savefig(os.path.join("output", "2mean_count.pdf"), bbox_inches="tight")
    
def fig4(gene_std, data_norm):
    y = "Mean mRNA"
    low_var_norm = data_norm[gene_std.index[gene_std < 5]]
    df = low_var_norm.mean(axis=1).to_frame(y).reset_index()
    
    fig = plt.figure(figsize=(10, 3.5))
    
    ax1 = fig.add_subplot(1, 2, 1)
    sns.scatterplot(df, x="x", y="y", hue=y, palette="Reds", hue_norm=(0, 2), ax=ax1)
    ax1.set(xticks=[], yticks=[])
    ax1.spines[["left", "bottom"]].set_visible(False)
    
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.scatter(df.x, df.y, df["Mean mRNA"], c=df["Mean mRNA"])
    ax2.set(xlabel="x", ylabel="y")
    fig.savefig(os.path.join("output", "2mean_count_norm.pdf"), bbox_inches="tight")
    
    
def fig5(gene_std, data_norm):
    fig, axes = plt.subplots(2, 3, figsize=(10, 5))
    for i, ax in enumerate(axes.flat):
        gene = gene_std.index[i]
        df = data_norm[[gene]].reset_index()
        scatter = sns.scatterplot(df, x="x", y="y", hue=gene, ax=ax)
        ax.legend().set_visible(False)
        ax.set(xticks=[], yticks=[], title=gene, xlabel="", ylabel="")
        ax.spines[["left", "bottom"]].set_visible(False)

    handles, labels = scatter.get_legend_handles_labels()
    fig.legend(handles, labels, loc="center right", title="mRNA")

    fig.tight_layout(rect=[0, 0, 0.95, 1])
    fig.savefig(os.path.join("output", "2gene_space_norm.pdf"), bbox_inches="tight")
    

if __name__ == "__main__":
    data = prepare_data()
    fig3(data)
    gene_std, data_norm = normalize_data(data)
    fig4(gene_std, data_norm)
    fig5(gene_std, data_norm)