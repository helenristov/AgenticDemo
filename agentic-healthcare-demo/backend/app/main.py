from fastapi import FastAPI
from .models import ChatRequest, ChatResponse, Citation
from .langchain_agent import run_agent
import uuid

app = FastAPI()

@app.get("/mock-live/eligibility/{member_id}")
async def mock_eligibility(member_id: str):
    return {"member_id": member_id, "eligibility": "ACTIVE"}

@app.get("/mock-live/claims/{claim_id}")
async def mock_claim(claim_id: str):
    return {"claim_id": claim_id, "status": "DENIED"}

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    answer, citations_raw = await run_agent(req.message, req.context)
    citations = [Citation(**c) for c in citations_raw]
    return ChatResponse(
        session_id=req.session_id,
        answer=answer,
        citations=citations,
        crm_writeback_id=f"crm_{uuid.uuid4().hex[:6]}"
    )
