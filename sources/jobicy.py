
import requests

URL = "https://jobicy.com/api/v2/remote-jobs"
HEADERS = {"User-Agent": "Mozilla/5.0 (veille-opportunites-agent)"}


def fetch() -> list[dict]:
    try:
        resp = requests.get(
            URL, headers=HEADERS, timeout=15,
            params={"count": 50, "industry": "engineering"},
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"[jobicy] Erreur de récupération : {e}")
        return []

    offres = []
    for item in data.get("jobs", []):
        offres.append({
            "titre": item.get("jobTitle", ""),
            "entreprise": item.get("companyName", ""),
            "lieu": item.get("jobGeo", "Remote"),
            "lien": item.get("url", ""),
            "date": item.get("pubDate", ""),
            "source": "Jobicy",
            "description": item.get("jobExcerpt", "") or item.get("jobDescription", "")[:500],
        })
    return offres
