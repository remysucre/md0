.PHONY: all clean test

all: index.html

index.html: README.md
	pandoc README.md -s -o index.html --metadata title="md0: simple markdown subset for painless parsing and rendering" -V mainfont="sans-serif"

test:
	python render.py

clean:
	rm -f index.html
