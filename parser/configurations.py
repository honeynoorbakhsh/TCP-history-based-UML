from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DIAGS_DIR = BASE_DIR / "diagrams"
SEQ_DIAGS_DIR = DIAGS_DIR / "sequence_diagrams"
ACT_DIAGS_DIR = DIAGS_DIR / "activity_diagrams"
SCENARIOS_FILE = BASE_DIR / "scenarios" / "steps.py"

