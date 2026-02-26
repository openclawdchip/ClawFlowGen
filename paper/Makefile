# Makefile for Science Paper Submission
# Generates PDF with all figures

# Tools
LATEX = pdflatex
BIBTEX = bibtex
CONVERT = convert

# Directories
FIGDIR = figures
OUTDIR = build

# Main file
MAIN = science_submission

# Figure files
FIGURES = $(wildcard $(FIGDIR)/*.tex)
FIGURE_PDFS = $(FIGURES:.tex=.pdf)
FIGURE_PNGS = $(FIGURES:.tex=.png)

# Default target
all: $(OUTDIR)/$(MAIN).pdf

# Create output directory
$(OUTDIR):
	mkdir -p $(OUTDIR)

# Compile main paper with figures inline (using standalone)
$(OUTDIR)/$(MAIN).pdf: $(MAIN).tex $(FIGDIR)/figures.tex | $(OUTDIR)
	@echo "Compiling main paper..."
	cd $(OUTDIR) && $(LATEX) -shell-escape ../$(MAIN).tex
	cd $(OUTDIR) && $(LATEX) -shell-escape ../$(MAIN).tex
	@echo "PDF generated: $@"

# Generate combined figures file
$(FIGDIR)/figures.tex: $(FIGURES)
	@echo "% Auto-generated figures file" > $@
	@echo "% Do not edit manually" >> $@

# Individual figure PDFs
$(FIGDIR)/%.pdf: $(FIGDIR)/%.tex
	@echo "Generating figure: $@"
	cd $(FIGDIR) && $(LATEX) -interaction=batchmode $(notdir $<) >/dev/null 2>&1 || true
	cd $(FIGDIR) && $(LATEX) -interaction=batchmode $(notdir $<) >/dev/null 2>&1 || true
	@mv $(FIGDIR)/$(basename $(notdir $@)).pdf $@ 2>/dev/null || true

# Convert figures to PNG for web
figures-png: $(FIGURE_PNGS)

$(FIGDIR)/%.png: $(FIGDIR)/%.pdf
	@echo "Converting to PNG: $@"
	$(CONVERT) -density 300 $< -quality 90 $@ 2>/dev/null || echo "ImageMagick not available, skipping PNG conversion"

# Submission package
submission: all
	@echo "Creating submission package..."
	mkdir -p submission
	cp $(OUTDIR)/$(MAIN).pdf submission/manuscript.pdf
	cp $(MAIN).tex submission/
	cp -r $(FIGDIR) submission/
	@echo "Submission package ready in submission/"

# Clean build files
clean:
	rm -rf $(OUTDIR)
	rm -f $(FIGDIR)/*.aux $(FIGDIR)/*.log $(FIGDIR)/*.pdf
	rm -f *.aux *.log *.out *.toc
	rm -rf submission/

# Clean all including PNGs
distclean: clean
	rm -f $(FIGDIR)/*.png

# Help
help:
	@echo "Science Paper Submission Makefile"
	@echo "================================="
	@echo ""
	@echo "Targets:"
	@echo "  make all        - Compile main paper PDF"
	@echo "  make figures    - Generate individual figure PDFs"
	@echo "  make figures-png- Convert figures to PNG format"
	@echo "  make submission - Create complete submission package"
	@echo "  make clean      - Remove build files"
	@echo "  make distclean  - Remove all generated files"
	@echo ""
	@echo "Output:"
	@echo "  build/science_submission.pdf - Main manuscript"
	@echo "  submission/                   - Complete submission package"

.PHONY: all figures figures-png submission clean distclean help
