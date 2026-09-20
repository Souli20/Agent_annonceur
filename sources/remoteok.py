

import requests

URL = "https://remoteok.com/api"
HEADERS = {"User-Agent": "Mozilla/5.0 (veille-opportunites-agent)"}


def fetch() -> list[dict]:
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[remoteok] Erreur de récupération : {e}")
        return []

    # Le premier élément est souvent un objet de métadonnées, pas une offre
    offres = []
    for item in data:
        if not isinstance(item, dict) or "id" not in item or "position" not in item:
            continue
        offres.append({
            "titre": item.get("position", ""),
            "entreprise": item.get("company", ""),
            "lieu": item.get("location", "Remote"),
            "lien": item.get("url", ""),
            "date": item.get("date", ""),
            "source": "RemoteOK",
            "description": item.get("description", "")[:500],
        })
    return offres
