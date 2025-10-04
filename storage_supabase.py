import os
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_user(user_id: int):
    resp = supabase.table("users").select("pontos,nivel").eq("user_id", user_id).maybe_single().execute()
    item = getattr(resp, "data", None)
    if item:
        return {"pontos": int(item.get("pontos", 0)), "nivel": int(item.get("nivel", 1))}
    return {"pontos": 0, "nivel": 1}

def update_points(user_id: int, acerto: bool):
    stats = get_user(user_id)
    pontos = stats["pontos"] + (10 if acerto else 0)
    nivel = pontos // 50 + 1
    payload = {"user_id": user_id, "pontos": pontos, "nivel": nivel}
    supabase.table("users").upsert(payload).execute()
    return {"pontos": pontos, "nivel": nivel}

def get_ranking(limit: int = 10):
    resp = supabase.table("users").select("user_id,pontos,nivel").order("pontos", desc=True).limit(limit).execute()
    data = getattr(resp, "data", []) or []
    return [(int(item["user_id"]), int(item["pontos"]), int(item["nivel"])) for item in data]
