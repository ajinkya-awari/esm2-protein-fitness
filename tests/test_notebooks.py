import json
from pathlib import Path


def test_kaggle_notebook_is_valid_nbformat_json_with_manual_cells():
    notebook_path = Path(__file__).parents[1] / "notebooks" / "kaggle_esm2_protein.ipynb"

    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))

    assert notebook["nbformat"] == 4
    assert notebook["nbformat_minor"] == 5
    assert len(notebook["cells"]) >= 10
    assert {cell["cell_type"] for cell in notebook["cells"]} == {"markdown", "code"}
    assert all(len("".join(cell["source"])) < 3000 for cell in notebook["cells"])


def test_kaggle_runbook_names_approval_gate_and_stop_conditions():
    runbook_path = Path(__file__).parents[1] / "notebooks" / "KAGGLE_RUNBOOK_esm2_protein.md"

    text = runbook_path.read_text(encoding="utf-8")

    assert "Approval" in text
    assert "Stop conditions" in text
    assert "do not download ProteinGym or model checkpoints" in text
