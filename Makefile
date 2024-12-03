.PHONY: clean

output/report.pdf: latex/report.tex \
		output/1gene_space.pdf \
		output/2gene_space_norm.pdf \
		output/3gpca_params.pdf
	pdflatex -output-directory output latex/report.tex
# unable to render reference in the first run
	pdflatex -output-directory output latex/report.tex

output/1gene_space.pdf output/1gene_std.pdf: r1variable.py
	python3 r1variable.py

output/2gene_space_norm.pdf output/2mean_count_norm.pdf output/2mean_count.pdf: r2mean.py
	python3 r2mean.py

output/3gpca_params.pdf output/3pca_gpca_compare.pdf: r3cluster.py
	python3 r3cluster.py

clean: 
	rm output/*