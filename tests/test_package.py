def test_package_imports_without_optional_dependencies():
    import esm2_fitness

    assert esm2_fitness.__version__ == "0.1.0"
