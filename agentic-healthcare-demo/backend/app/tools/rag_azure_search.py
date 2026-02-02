import json
from typing import Dict, Any, List
from ..models import Citation

def local_fallback_rag(query: str, filters: Dict[str, Any]) -> List[Citation]:
    hits = []
    with open("app/data/policies.jsonl") as f:
        for line in f:
            doc = json.loads(line)
            if query.lower() in doc["content"].lower():
                hits.append(Citation(
                    doc_id=doc["doc_id"],
                    title=doc["title"],
                    snippet=doc["content"][:300],
                    metadata={k: doc.get(k) for k in ["plan_type","state","effective_date"]}
                ))
            if len(hits) >= 3:
                break
    return hits
