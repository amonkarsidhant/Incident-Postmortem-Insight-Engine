import json
from datetime import date
from pathlib import Path


EVALUATION_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "severity": {"type": "string"},
        "action_items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "owner": {"type": "string"},
                    "due_date": {"type": "string", "format": "date"}
                },
                "required": ["description", "owner", "due_date"],
            },
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
        },
    },
    "required": ["summary", "severity", "action_items", "tags"],
}


MOCK_TAGS = ["database", "regression", "customer-impact"]


def evaluate_postmortem(file_path: str) -> dict:
    _ = Path(file_path)  # placeholder for future file processing

    evaluation = {
        "summary": "Automated evaluation of postmortem file.",
        "severity": "medium",
        "action_items": [
            {
                "description": "Review database failover procedures.",
                "owner": "infrastructure-team",
                "due_date": date.today().isoformat(),
            }
        ],
        "tags": MOCK_TAGS,
    }
    return json.loads(json.dumps(evaluation))
