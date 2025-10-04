from supabase import create_client

def create_supabase_client():
    url = "https://YOUR_SUPABASE_URL.supabase.co"
    key = "YOUR_SUPABASE_KEY"
    return create_client(url, key)

supabase = create_supabase_client()

def get_user(user_id):
    data = supabase.table("usuarios").select("*").eq("user_id", user_id).execute()
    if data.data:
        return data.data[0]
    else:
        return None

def update_points(user_id, points):
    user = get_user(user_id)
    if user:
        total = user["pontos"] + points
        supabase.table("usuarios").update({"pontos": total}).eq("user_id", user_id).execute()
    else:
        supabase.table("usuarios").insert({"user_id": user_id, "pontos": points}).execute()

def get_ranking():
    data = supabase.table("usuarios").select("*").order("pontos", desc=True).limit(10).execute()
    return data.data
