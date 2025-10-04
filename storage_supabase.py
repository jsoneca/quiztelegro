import os
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_user(user_id):
    res = supabase.table("usuarios").select("*").eq("user_id", user_id).execute()
    if res.data:
        return res.data[0]
    else:
        supabase.table("usuarios").insert({"user_id": user_id, "pontos": 0, "nivel": 1}).execute()
        return {"user_id": user_id, "pontos": 0, "nivel": 1}

def update_points(user_id, pontos_ganhos):
    user = get_user(user_id)
    novos_pontos = user["pontos"] + pontos_ganhos
    nivel = user["nivel"]
    pontos_para_subir = 100 * nivel

    while novos_pontos >= pontos_para_subir:
        novos_pontos -= pontos_para_subir
        nivel += 1
        pontos_para_subir = 100 * nivel

    supabase.table("usuarios").update({"pontos": novos_pontos, "nivel": nivel}).eq("user_id", user_id).execute()

def get_ranking():
    res = supabase.table("usuarios").select("user_id, pontos, nivel").order("nivel", desc=True).execute()
    return res.data
