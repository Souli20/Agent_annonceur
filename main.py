"""
Point d'entrée de l'agent de veille d'opportunités.

Utilisation :
    python main.py

Enchaîne : collecte des sources actives -> filtrage par mots-clés ->
suppression des doublons déjà notifiés -> envoi email / WhatsApp.
"""

import importlib

from config import ACTIVE_SOURCES, EMAIL_ENABLED, WHATSAPP_ENABLED
from filtre import filtrer
from db import filtrer_nouvelles


def collecter_toutes_les_offres() -> list[dict]:
    toutes_offres = []
    for nom_source in ACTIVE_SOURCES:
        try:
            module = importlib.import_module(f"sources.{nom_source}")
            offres = module.fetch()
            print(f"[collecte] {nom_source} : {len(offres)} offre(s) brute(s)")
            toutes_offres.extend(offres)
        except Exception as e:
            print(f"[collecte] Erreur sur la source '{nom_source}' : {e}")
    return toutes_offres


def main():
    print("=== Agent de veille d'opportunités ===")

    offres_brutes = collecter_toutes_les_offres()
    print(f"Total brut : {len(offres_brutes)} offre(s)")

    offres_pertinentes = filtrer(offres_brutes)
    print(f"Après filtrage par mots-clés : {len(offres_pertinentes)} offre(s)")

    offres_nouvelles = filtrer_nouvelles(offres_pertinentes)
    print(f"Nouvelles (jamais notifiées) : {len(offres_nouvelles)} offre(s)")

    if not offres_nouvelles:
        print("Rien de nouveau à envoyer.")
        return

    if EMAIL_ENABLED:
        from notifier import email_sender
        email_sender.envoyer(offres_nouvelles)

    if WHATSAPP_ENABLED:
        from notifier import whatsapp_sender
        whatsapp_sender.envoyer(offres_nouvelles)

    print("=== Terminé ===")


if __name__ == "__main__":
    main()
