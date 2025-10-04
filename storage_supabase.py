import os
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def salvar_usuario(user_id, username):
    url = f"{SUPABASE_URL}/rest/v1/usuarios"
    data = {"user_id": str(user_id), "username": username}
    get_res = requests.get(url, headers=headers, params={"user_id": f"eq.{user_id}"})
    if get_res.status_code == 200 and len(get_res.json()) > 0:
        return
    res = requests.post(url, headers=headers, json=data)
    if res.status_code not in (200, 201):
        print("Erro ao salvar usuário:", res.text)

def atualizar_pontos(user_id, pontos_ganhos):
    url = f"{SUPABASE_URL}/rest/v1/usuarios"
    get_res = requests.get(url, headers=headers, params={"user_id": f"eq.{user_id}"})
    if get_res.status_code != 200 or len(get_res.json()) == 0:
        print("Usuário não encontrado.")
        return
    usuario = get_res.json()[0]
    novos_pontos = usuario.get("pontos", 0) + pontos_ganhos
    novo_nivel = usuario.get("nivel", 1)
    if novos_pontos >= novo_nivel * 100:
        novo_nivel += 1
    patch_data = {"pontos": novos_pontos, "nivel": novo_nivel}
    res = requests.patch(f"{url}?user_id=eq.{user_id}", headers=headers, json=patch_data)
    if res.status_code not in (200, 204):
        print("Erro ao atualizar pontos:", res.text)

def obter_usuario(user_id):
    url = f"{SUPABASE_URL}/rest/v1/usuarios"
    res = requests.get(url, headers=headers, params={"user_id": f"eq.{user_id}"})
    if res.status_code == 200 and len(res.json()) > 0:
        return res.json()[0]
    else:
        return None
