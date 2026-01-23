.PHONY: setup test clean

setup:
	uv sync --extra dev

test:
	pytest

clean:
	rm -rf .venv