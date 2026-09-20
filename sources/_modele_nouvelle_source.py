

import requests
from bs4 import BeautifulSoup

URL = "https://exemple-site-emploi.com/recherche?q=data"
HEADERS = {"User-Agent": "Mozilla/5.0 (veille-opportunites-agent)"}


def fetch() -> list[dict]:
    try:
        resp = requests.get(URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"[modele] Erreur de récupération : {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    offres = []

    # --- À ADAPTER : ceci est un exemple générique, inspecte le HTML réel
    # du site (clic droit > Inspecter) pour trouver les bons sélecteurs.
    for carte in soup.select(".offre-emploi"):  # sélecteur CSS à adapter
        titre_tag = carte.select_one(".titre-offre")
        lien_tag = carte.select_one("a")
        entreprise_tag = carte.select_one(".entreprise")

        if not titre_tag or not lien_tag:
            continue

        offres.append({
            "titre": titre_tag.get_text(strip=True),
            "entreprise": entreprise_tag.get_text(strip=True) if entreprise_tag else "",
            "lieu": "",
            "lien": lien_tag.get("href", ""),
            "date": "",
            "source": "ModèleSource",
            "description": "",
        })

    return offres
