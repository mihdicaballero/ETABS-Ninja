DOCS_DIR = docs

docs:
	pdoc --html etabsninja --output-dir $(DOCS_DIR) --force

clean_docs:
	rmdir /s /q $(DOCS_DIR)

.PHONY: docs clean_docs

