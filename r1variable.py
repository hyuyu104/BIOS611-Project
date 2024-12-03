import os
import seaborn as sns
from matplotlib import pyplot as plt

from utils import prepare_data


def fig1(data, out="output"):
    gene_std = data.std().sort_values(ascending=False)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3))
    sns.histplot(gene_std[gene_std > 1], ax=axes[0])
    df = (
        gene_std[:10]
        .to_frame("std")
        .reset_index(names=["gene"])
        .reset_index(names=["x"])
    )
    sns.scatterplot(df, x="x", y="std", ax=axes[1], color="darkorange", s=50)
    for i, r in df.iterrows():
        axes[1].vlines(r["x"], 0, r["std"], color="darkorange")
    axes[1].set(xticks=df.x, xticklabels=df.gene)
    axes[1].tick_params(axis='x', rotation=30)
    ylim = (0, gene_std.max()*1.1)
    axes[1].set(xlabel="", ylabel="Standard deviation", ylim=ylim)
    if not os.path.exists(out):
        os.mkdir(out)
    fig.savefig(os.path.join(out, "1gene_std.pdf"), bbox_inches="tight")
    
    
def fig2(data, out="output"):
    gene_std = data.std().sort_values(ascending=False)
    fig, axes = plt.subplots(2, 3, figsize=(10, 5))
    for i, ax in enumerate(axes.flat):
        gene = gene_std.index[i]
        df = data[[gene]].reset_index()
        scatter = sns.scatterplot(df, x="x", y="y", hue=gene, ax=ax)
        ax.legend().set_visible(False)
        ax.set(xticks=[], yticks=[], title=gene, xlabel="", ylabel="")
        ax.spines[["left", "bottom"]].set_visible(False)

    handles, labels = scatter.get_legend_handles_labels()
    fig.legend(handles, labels, loc="center right", title="mRNA")

    fig.tight_layout(rect=[0, 0, 0.95, 1])
    fig.savefig(os.path.join(out, "1gene_space.pdf"), bbox_inches="tight")
    
    
if __name__ == "__main__":
    data = prepare_data()
    fig1(data)
    fig2(data)