import json
from functools import lru_cache
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


@lru_cache
def load_role_skill_matrix() -> dict:
    with (DATA_DIR / "role_skill_matrix.json").open("r", encoding="utf-8") as file:
        return json.load(file)


@lru_cache
def load_learning_resources() -> list[dict]:
    with (DATA_DIR / "learning_resources.json").open("r", encoding="utf-8") as file:
        return json.load(file)
