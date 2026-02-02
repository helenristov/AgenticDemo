import time
import json
import httpx
import streamlit as st

# -----------------------------
# Page + styling
# -----------------------------
st.set_page_config(page_title="Agent Copilot Demo", layout="wide")

CUSTOM_CSS = """
<style>
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
.small-muted { color: rgba(49, 51, 63, 0.65); font-size: 0.9rem; }
.card {
  border: 1px solid rgba(49, 51, 63, 0.12);
  border-radius: 14px;
  padding: 16px 16px;
  background: #ffffff;
}
.badge {
  display:inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  border: 1px solid rgba(49, 51, 63, 0.15);
  font-size: 0.85rem;
  margin-right: 6px;
  background: #f8fafc;
}
.section-title { margin: 0.4rem 0 0.2rem 0; font-weight: 650; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# -----------------------------
# Demo scenarios (4)
# -----------------------------
SCENARIOS = {
    "1) Coverage & Prior Auth (RAG + LLM)": {
        "default_question": "Is outpatient physical therapy covered, and does it require prior authorization?",
        "default_member_id": "M123",
        "default_claim_id": "",
        "talk_track": "The model isn’t inventing coverage — it’s grounded on retrieved policy documents with citations.",
        "proves": "RAG • Hallucination control • Healthcare realism • Grounded synthesis",
        "expects": "policy_search → policy excerpts → citations",
    },
    "2) Eligibility Check (Live Tool)": {
        "default_question": "Is this member currently eligible?",
        "default_member_id": "M123",
        "default_claim_id": "",
        "talk_track": "Eligibility always comes from a live system — never from the LLM.",
        "proves": "Tool routing • Real-time data • Separation of concerns",
        "expects": "get_eligibility → ACTIVE/INACTIVE",
    },
    "3) Claim Denial Explanation (Tool + LLM)": {
        "default_question": "Why was this claim denied and what are the next steps?",
        "default_member_id": "M123",
        "default_claim_id": "C999",
        "talk_track": "The LLM explains outcomes, but it doesn’t decide them.",
        "proves": "Explainability • Compliance-safe LLM usage • Agent + tool cooperation",
        "expects": "get_claim_status → denial reason → plain-language explanation",
    },
    "4) Multi-Intent Orchestration": {
        "default_question": "Is outpatient PT covered and is this member eligible?",
        "default_member_id": "M123",
        "default_claim_id": "",
        "talk_track": "The agent breaks a single question into multiple actions and routes each appropriately.",
        "proves": "True agent behavior • Multi-tool reasoning • Orchestration",
        "expects": "policy_search + get_eligibility → combined answer",
    },
}

# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar:
    st.header("⚙️ Demo Controls")
    backend_url = st.text_input("Backend URL", "http://localhost:8000")
    timeout_s = st.slider("Timeout (seconds)", 20, 180, 120, 10)
    show_debug = st.checkbox("Show debug JSON", value=False)

    st.markdown("---")
    st.header("🎬 Scenario Picker")
    scenario_name = st.selectbox("Choose scenario", list(SCENARIOS.keys()))
    scenario = SCENARIOS[scenario_name]

    st.markdown("**Talk track**")
    st.info(f"“{scenario['talk_track']}”")

    st.markdown("**What this proves**")
    st.write(scenario["proves"])

    st.markdown("**Expected behavior**")
    st.code(scenario["expects"])

# -----------------------------
# Header
# -----------------------------
st.markdown(
    """
<div class="card">
  <div style="display:flex; justify-content:space-between; align-items:flex-start;">
    <div>
      <h2 style="margin:0;">🧠 Agent Copilot Demo</h2>
      <div class="small-muted">Scenario-driven UI for Coverage (RAG), Eligibility, Claims, and Multi-intent orchestration</div>
    </div>
    <div>
      <span class="badge">FastAPI</span>
      <span class="badge">LangChain Agent</span>
      <span class="badge">RAG + Tools</span>
      <span class="badge">CRM Write-back</span>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# -----------------------------
# Main layout
# -----------------------------
left, right = st.columns([0.45, 0.55], gap="large")

# Session + context defaults per scenario
with left:
    st.markdown("### 🧾 Case Context")
    session_id = st.text_input("Session ID", "s1")

    c1, c2 = st.columns(2)
    with c1:
        member_id = st.text_input("Member ID", scenario["default_member_id"])
    with c2:
        claim_id = st.text_input("Claim ID (optional)", scenario["default_claim_id"])

    st.markdown("### ❓ Question")
    q = st.text_area("Ask the copilot", scenario["default_question"], height=120)

    # Show what the agent will receive
    context = {"member_id": member_id}
    if claim_id.strip():
        context["claim_id"] = claim_id.strip()

    st.markdown("### 📦 Payload Preview")
    payload = {"session_id": session_id, "message": q, "context": context}
    st.code(json.dumps(payload, indent=2), language="json")

    ask = st.button("Ask Agent", type="primary", use_container_width=True)

    with st.expander("Tips if a tool call doesn’t trigger"):
        st.write("• Use explicit keywords: coverage, prior auth, eligible, claim status")
        st.write("• Include a claim_id for claim denial demos")
        st.write("• Increase timeout if your model is slow")

with right:
    st.markdown("### 📋 Results")

    if ask:
        try:
            t0 = time.time()
            with st.spinner("Calling backend and running agent..."):
                with httpx.Client(timeout=httpx.Timeout(timeout_s, connect=10.0)) as client:
                    r = client.post(f"{backend_url.rstrip('/')}/chat", json=payload)
            latency_ms = int((time.time() - t0) * 1000)

            st.caption(f"HTTP {r.status_code} • {r.headers.get('content-type','')} • {latency_ms} ms")

            # If backend didn't return JSON, show raw and stop safely.
            ctype = (r.headers.get("content-type") or "").lower()
            if "application/json" not in ctype:
                st.error("Backend response is not JSON (showing raw text).")
                st.code(r.text[:4000])
                st.stop()

            data = r.json()

            # Pull fields
            answer = data.get("answer", "")
            citations = data.get("citations") or []
            tool_results = data.get("tool_results") or []
            crm_id = data.get("crm_writeback_id")

            # Answer card
            st.markdown("#### ✅ Answer")
            st.markdown(f"<div class='card'>{answer}</div>", unsafe_allow_html=True)

            # 3-column details
            a, b, c = st.columns([1, 1, 1], gap="large")

            with a:
                st.markdown("#### 📎 Citations")
                if citations:
                    # Keep it compact, but readable
                    for ci in citations:
                        doc = ci.get("doc_id", "doc")
                        title = ci.get("title", "")
                        snippet = ci.get("snippet", "")
                        st.markdown(f"**{doc}** {title}")
                        if snippet:
                            st.caption(snippet[:240] + ("..." if len(snippet) > 240 else ""))
                        st.write("---")
                else:
                    st.info("No citations returned.")

            with b:
                st.markdown("#### 🧰 Tool Calls")
                if tool_results:
                    st.json(tool_results)
                else:
                    st.info("No tool results returned.")

            with c:
                st.markdown("#### 🗂️ CRM Write-back")
                if crm_id:
                    st.success(f"Created note: {crm_id}")
                else:
                    st.info("No CRM write-back id returned.")

            if show_debug:
                st.markdown("#### 🐛 Debug (raw JSON)")
                st.json(data)

        except httpx.ReadTimeout:
            st.error("Timed out. Increase the timeout slider or check your backend logs.")
        except Exception as e:
            st.exception(e)

# -----------------------------
# Quick launcher view
# -----------------------------
st.write("")
st.markdown("### 🚀 Quick Scenario Launcher")
tabs = st.tabs(list(SCENARIOS.keys()))
for i, name in enumerate(SCENARIOS.keys()):
    s = SCENARIOS[name]
    with tabs[i]:
        st.markdown(f"**Prompt:** {s['default_question']}")
        st.markdown(f"**Talk track:** “{s['talk_track']}”")
        st.markdown(f"**Proves:** {s['proves']}")
        st.caption("Use Member ID M123. Use Claim ID C999 for claim scenario.")
