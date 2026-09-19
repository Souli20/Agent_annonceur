"""
Filtrage des offres par pertinence (mots-clés inclus/exclus).
"""

from config import KEYWORDS_INCLUDE, KEYWORDS_EXCLUDE


def est_pertinente(offre: dict) -> bool:
    texte = f"{offre.get('titre', '')} {offre.get('description', '')}".lower()

    if any(mot.lower() in texte for mot in KEYWORDS_EXCLUDE):
        return False

    return any(mot.lower() in texte for mot in KEYWORDS_INCLUDE)


def filtrer(offres: list[dict]) -> list[dict]:
    return [o for o in offres if est_pertinente(o)]
