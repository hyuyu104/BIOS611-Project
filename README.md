BIOS 611 Project
----------------

### How to use this repository

Create docker container and generate the report:
```sh
docker build . -t project
docker run --rm -v "$(pwd):/workspace" project make
```
The generated report is located at `output/report.pdf`. For reference, the generated one should look the same as the one at `latex/report.pdf`.

Clean the output:
```sh
docker run --rm -v "$(pwd):/workspace" project make clean
```

### Background

This is a spatial transcriptomic dataset, which contains the gene expression data (~15,000 genes) at ~250 position in a human breast cancer tissue. The original study can be found [here](https://www.science.org/doi/10.1126/science.aaf2403). The processed data is downloaded from [this repository](https://github.com/xzhoulab/SPARK/blob/master/data/Layer2_BC_Count.rds). Briefly, the data is a $15,000\times 250$ table, with each column being a spatial location, and each row being the mRNA count of a gene at each spatial location.

Possible questions to investigate:

1. Do locations that are closer to each other have similar gene expression profile?

2. Are there regions with abnormal gene expression profile compared to other regions?

3. What are the genes differentially expressed between different regions?

4. Can we segment the tissue via differentially expressed genes into several regions?

5. Does locations at the edge of the region have lower data quality compared to the interior regions?