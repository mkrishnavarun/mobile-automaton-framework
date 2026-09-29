from pathlib import Path

import yaml


class TestDataLoader:
    """Loads test data from YAML files."""

    @staticmethod
    def load(file_name: str) -> dict:
        project_root = Path(__file__).resolve().parent.parent
        file_path = project_root / "test_data" / file_name

        if not file_path.exists():
            raise FileNotFoundError(
                f"Test data file not found: {file_path}"
            )

        with file_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file)