OBJS = thesis.tex

thesis: $(OBJS)
	latexmk -pdf $<

%.pdf: %.svg
	inkscape -D -z --file=$< --export-pdf=$@


.PHONY: all, clean
all: thesis

clean:
	latexmk -c
