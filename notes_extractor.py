import json
from pathlib import Path

# Import directly from src package
from baml_client import b, reset_baml_env_vars
from baml_client import types

from dotenv import load_dotenv
import os

load_dotenv()
os.environ["BAML_LOG"] = "WARN"
reset_baml_env_vars(dict(os.environ))


def extract_notes(notes: str) -> list[types.PatientInfo]:
    return b.ExtractMedicationInfo(notes)


if __name__ == "__main__":
    notes = Path("./data/text/notes_1.txt").read_text()
    # Model dump the result into a json file
    result = extract_notes(notes)
    with open("result.json", "w") as f:
        json.dump([item.model_dump() for item in result], f, indent=4)
