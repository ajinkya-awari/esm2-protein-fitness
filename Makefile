.PHONY: check synthetic gates test

check:
	PYTHONPATH=src python -m esm2_fitness.pipeline check

synthetic:
	PYTHONPATH=src python -m esm2_fitness.pipeline synthetic

gates:
	PYTHONPATH=src python -m esm2_fitness.pipeline gates

test:
	python -m pytest -q
