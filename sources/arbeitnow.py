"""
Source : Arbeitnow (https://arbeitnow.com)
API JSON publique et gratuite, pas de clé nécessaire. Bonne couverture
tech/data en Europe et remote.
"""

import requests

URL = "https://arbeitnow.com/api/job-board-api"
HEADERS = {"User-Agent": "Mozilla/5.0 (veille-opportunites-agent)"}


def fetch() -> list[dict]:
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[arbeitnow] Erreur de récupération : {e}")
        return []

    offres = []
    for item in data.get("data", []):
        offres.append({
            "titre": item.get("title", ""),
            "entreprise": item.get("company_name", ""),
            "lieu": item.get("location") or ("Remote" if item.get("remote") else "N/A"),
            "lien": item.get("url", ""),
            "date": str(item.get("created_at", "")),
            "source": "Arbeitnow",
            "description": item.get("description", "")[:500],
        })
    return offres
