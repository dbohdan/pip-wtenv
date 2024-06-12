README.md: README.template.md build.py pip_wtenv.py
	./build.py

test:
	./test_pip_wtenv.py

.PHONY: test
