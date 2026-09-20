

import requests

URL = "https://remotive.com/api/remote-jobs"
HEADERS = {"User-Agent": "Mozilla/5.0 (veille-opportunites-agent)"}


def fetch() -> list[dict]:
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=15, params={"category": "data"})
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[remotive] Erreur de récupération : {e}")
        return []

    offres = []
    for item in data.get("jobs", []):
        offres.append({
            "titre": item.get("title", ""),
            "entreprise": item.get("company_name", ""),
            "lieu": item.get("candidate_required_location", "Remote"),
            "lien": item.get("url", ""),
            "date": item.get("publication_date", ""),
            "source": "Remotive",
            "description": item.get("description", "")[:500],
        })
    return offres
