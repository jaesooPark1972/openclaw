import sys
from pathlib import Path

PROJECT_ROOT = Path("f:/AGen")
sys.path.append(str(PROJECT_ROOT))

try:
    from modules.engine.engine_ontology import get_orchestrator, EngineType
    print("SUCCESS: Orchestrator and EngineType imported.")
    orch = get_orchestrator()
    print(f"Orchestrator initialized. Engines count: {len(orch.ontology)}")
except Exception as e:
    print(f"FAILURE: {e}")
