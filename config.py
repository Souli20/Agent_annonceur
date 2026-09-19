"""
Configuration centrale de l'agent de veille.
Toutes les valeurs sensibles (mots de passe, tokens) viennent des variables
d'environnement (voir .env.example) — ne jamais les écrire en dur ici.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()  # charge le fichier .env s'il existe (ignoré en silence sinon)
except ImportError:
    pass

# --- Mots-clés de pertinence -------------------------------------------------
# Une offre est retenue si son titre OU sa description contient au moins un
# mot-clé de KEYWORDS_INCLUDE et aucun mot-clé de KEYWORDS_EXCLUDE.
KEYWORDS_INCLUDE = [
    "data", "statistic", "statistique", "économ", "econom",
    "économétrie", "econometric", "analyst", "analyste",
    "data scientist", "data analyst", "quantitative", "ise",
    "stage", "internship", "junior",
]

KEYWORDS_EXCLUDE = [
    "senior", "10+ years", "director", "directeur général",
]

# --- Base de données locale (déduplication) ----------------------------------
DB_PATH = os.getenv("DB_PATH", "offres_vues.db")

# --- Email --------------------------------------------------------------------
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "true").lower() == "true"
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")          # ton adresse Gmail
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # mot de passe d'application (pas ton mdp normal)
EMAIL_TO = os.getenv("EMAIL_TO", "")            # adresse de réception

# --- WhatsApp (via Twilio) -----------------------------------------------------
WHATSAPP_ENABLED = os.getenv("WHATSAPP_ENABLED", "false").lower() == "true"
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+14155238886")  # sandbox Twilio par défaut
WHATSAPP_TO = os.getenv("WHATSAPP_TO", "")  # format: whatsapp:+22606449610

# --- Sources actives ------------------------------------------------------------
# Chaque source a une fonction fetch() dans sources/<nom>.py qui renvoie une
# liste de dicts uniformes: {titre, entreprise, lieu, lien, date, source, description}
ACTIVE_SOURCES = ["remoteok", "remotive"]
