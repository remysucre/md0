.PHONY: all clean test

all: index.html

index.html: README.md
	pandoc README.md -s -o index.html --metadata title="md0: Simple Markdown Subset for Painless Parsing and Rendering"

test:
	python render.py

clean:
	rm -f index.html
