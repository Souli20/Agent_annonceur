"""
Envoi de notifications WhatsApp via l'API Twilio.

Prérequis :
- Compte Twilio (https://www.twilio.com/whatsapp) + numéro sandbox ou officiel
- pip install twilio
- Variables d'environnement TWILIO_ACCOUNT_SID / TWILIO_AUTH_TOKEN /
  TWILIO_WHATSAPP_FROM / WHATSAPP_TO (voir .env.example)

Note : un message WhatsApp classique est limité en taille. On envoie donc
un message par offre (ou un résumé si beaucoup d'offres).
"""

from config import (
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, WHATSAPP_TO
)


def envoyer(offres: list[dict]) -> None:
    if not offres:
        return

    try:
        from twilio.rest import Client
    except ImportError:
        print("[whatsapp] Le paquet 'twilio' n'est pas installé (pip install twilio)")
        return

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # Un seul message groupé si peu d'offres, sinon un résumé + lien vers l'email
    if len(offres) <= 5:
        corps = f"{len(offres)} nouvelle(s) opportunité(s) :\n\n" + "\n\n".join(
            f"• {o['titre']} — {o.get('entreprise', 'N/A')}\n{o.get('lien')}"
            for o in offres
        )
    else:
        corps = (
            f"{len(offres)} nouvelles opportunités trouvées ! "
            f"Détails envoyés par email."
        )

    client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        to=WHATSAPP_TO,
        body=corps,
    )
    print(f"[whatsapp] Notification envoyée à {WHATSAPP_TO}")
