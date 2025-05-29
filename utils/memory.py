import os
import json
from datetime import datetime

DECISIONS_FILE = "data/decisions.json"
PRDS_FILE = "data/prds.json"
OKR_ANALYSIS_FILE = "data/okr_analysis.json"

def _load_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def _save_file(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def create_entry(raw_text, summary):
    return {
        "timestamp": str(datetime.now()),
        "raw_text": raw_text,
        "summary": summary
    }

def save_decision(entry):
    data = _load_file(DECISIONS_FILE)
    data.append(entry)
    _save_file(DECISIONS_FILE, data)

def load_decisions():
    return _load_file(DECISIONS_FILE)

def clear_decisions():
    _save_file(DECISIONS_FILE, [])

def save_prd(prd_text):
    data = _load_file(PRDS_FILE)
    entry = {
        "timestamp": str(datetime.now()),
        "text": prd_text
    }
    data.append(entry)
    _save_file(PRDS_FILE, data)

def load_prds():
    return _load_file(PRDS_FILE)

def clear_prds():
    _save_file(PRDS_FILE, [])

def save_okr_analysis(entry):
    data = _load_file(OKR_ANALYSIS_FILE)
    data.append(entry)
    _save_file(OKR_ANALYSIS_FILE, data)

def load_okr_analyses():
    return _load_file(OKR_ANALYSIS_FILE)

def clear_okr_analyses():
    _save_file(OKR_ANALYSIS_FILE, [])
