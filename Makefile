.PHONY: check synthetic test

check:
	PYTHONPATH=src python -m esm2_fitness.pipeline check

synthetic:
	PYTHONPATH=src python -m esm2_fitness.pipeline synthetic

test:
	python -m pytest -q
