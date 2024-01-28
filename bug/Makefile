.PHONY: clean
PDFMAKER=pdflatex
DOC=document.pdf
ADOC=annotated.pdf
ODOC=ocr.pdf
PDOC=patched.pdf
XDOC=patched_ocr.pdf

%.pdf: %.tex
	$(PDFMAKER) $<

$(ODOC): $(ADOC)
	. .venv/bin/activate && ocrmypdf -v 1 --output-type pdf --skip-text --language eng $(ADOC) $(ODOC)

$(ADOC): $(DOC)
	. .venv/bin/activate && python add_dc_metadata.py $(DOC) $(ADOC)
	cp $(DOC) $(ADOC)
	exiftool -XMP-pdf:CreationDate=2023-12-25 -XMP-pdf:Title="Test Document" -XMP-pdf:Author="Someone" $(ADOC)
	. .venv/bin/activate && python add_dc_metadata.py $(DOC) $(ADOC)

$(PDOC): $(ADOC)
	. .venv/bin/activate && python patch_rdf.py $(ADOC) $(PDOC)

$(XDOC): $(PDOC)
	. .venv/bin/activate && ocrmypdf -v 1 --output-type pdfa --skip-text --language eng $(PDOC) $(XDOC)

clean:
	rm -f $(DOC) $(ADOC) $(ODOC) $(PDOC) $(XDOC)

