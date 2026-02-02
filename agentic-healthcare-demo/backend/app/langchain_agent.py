from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from .config import settings
from .tools.phi_redaction import minimize_phi
from .tools.rag_azure_search import local_fallback_rag
from .tools.live_api import eligibility_lookup, claim_status_lookup

@tool
async def policy_search(query: str):
    """
    Search policy and SOP documents and return relevant passages with citations.
    Use this tool for coverage, benefits, policy, or workflow questions.
    """
    cits = local_fallback_rag(query, {})
    return {"citations": [c.model_dump() for c in cits]}

@tool
async def get_eligibility(member_id: str):
    """
    Retrieve authoritative eligibility and coverage status for a member.
    """
    return await eligibility_lookup(member_id)


@tool
async def get_claim_status(claim_id: str):
    """
    Retrieve authoritative claim status and denial information.
    """
    return await claim_status_lookup(claim_id)

def build_agent():
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.2,
        timeout=30,
        max_retries=1,
        api_key=settings.OPENAI_API_KEY,  # explicit to avoid env-loading issues
    )

    tools = [policy_search, get_eligibility, get_claim_status]

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a healthcare call center assistant. Use tools when needed. Cite policy sources."),
        ("human", "{input}\nContext: {context}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_openai_functions_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        return_intermediate_steps=True,
        max_iterations=3,
        max_execution_time=25,
    )

async def run_agent(message: str, context: dict):
    minimized,_ = minimize_phi(message)
    agent = build_agent()
    result = await agent.ainvoke({"input": minimized, "context": context})
    citations = []
    for step in result.get("intermediate_steps", []):
        action, obs = step
        if action.tool == "policy_search":
            citations.extend(obs.get("citations", []))
    return result["output"], citations
