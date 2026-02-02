from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional

class Citation(BaseModel):
    doc_id: str
    title: str
    snippet: str
    url: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ToolResult(BaseModel):
    name: str
    data: Dict[str, Any]
    citations: List[Citation] = Field(default_factory=list)

class ChatRequest(BaseModel):
    session_id: str
    message: str
    context: Dict[str, Any] = Field(default_factory=dict)

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    citations: List[Citation] = Field(default_factory=list)
    tool_results: List[ToolResult] = Field(default_factory=list)
    crm_writeback_id: Optional[str] = None
