from fastapi import FastAPI, Query
from typing import Optional
import json
import os

app = FastAPI()

# Load data once at startup
with open("app/data/structure_knowledge.json") as f:
    structure_data = json.load(f)

with open("app/data/domain_knowledge.json") as f:
    domain_data = json.load(f)

@app.get("/get_sentence_templates")
def get_sentence_templates(
    function: str = Query(...),
    paragraph_type: Optional[str] = Query(None),
    limit: int = Query(3)
):
    results = []
    for entry in structure_data["sentence_templates"]:
        if entry["function"].lower() == function.lower():
            if paragraph_type and "paragraph_type" in entry:
                if entry["paragraph_type"].lower() != paragraph_type.lower():
                    continue
            results.append(entry)
        if len(results) >= limit:
            break
    return {"templates": results}

@app.get("/get_domain_elements")
def get_domain_elements(
    role: Optional[str] = Query(None),
    construct: Optional[str] = Query(None),
    citation_type: Optional[str] = Query(None)
):
    result = {}

    if role:
        result["model_structure"] = {k: v for k, v in domain_data["model_structure"]["level_2"].items() if k == role}

    if construct:
        if construct in domain_data["constructs"]:
            result["construct_info"] = {
                "name": construct,
                "mentions": domain_data["constructs"][construct]["mentions"]
            }

    if citation_type:
        result["citations"] = [
            c for c in domain_data["citations"]
            if c["type"].lower() == citation_type.lower()
        ]

    return result
