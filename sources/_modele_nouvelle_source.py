"""
MODÈLE — copie ce fichier vers sources/<nom_du_site>.py pour ajouter une
nouvelle source (ex: Emploi.cm, Jobartis, un portail BAD/PNUD...).

Chaque source doit exposer une fonction fetch() qui renvoie une liste de
dicts avec les mêmes clés que les autres sources :
{titre, entreprise, lieu, lien, date, source, description}

Étapes :
1. Renomme ce fichier (ex: sources/emploi_cm.py)
2. Adapte l'URL et le parsing ci-dessous à la structure réelle du site
3. Ajoute le nom du module dans config.ACTIVE_SOURCES (ex: "emploi_cm")
4. Respecte le robots.txt du site et ne fais pas trop de requêtes rapprochées
"""

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
