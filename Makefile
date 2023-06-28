DOCS_DIR = docs

docs:
	pdoc --html --output-dir $(DOCS_DIR) --force etabsninja
	xcopy $(DOCS_DIR)\etabsninja $(DOCS_DIR) /e /i /q
	rmdir /s /q $(DOCS_DIR)\etabsninja
	pdoc --http : etabsninja

clean_docs:
	rmdir /s /q $(DOCS_DIR)

.PHONY: docs clean_docs


