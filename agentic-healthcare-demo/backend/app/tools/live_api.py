import httpx
from ..config import settings

async def eligibility_lookup(member_id: str):
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{settings.LIVE_API_BASE_URL}/eligibility/{member_id}")
        r.raise_for_status()
        return r.json()

async def claim_status_lookup(claim_id: str):
    async with httpx.AsyncClient() as c:
        r = await c.get(f"{settings.LIVE_API_BASE_URL}/claims/{claim_id}")
        r.raise_for_status()
        return r.json()
