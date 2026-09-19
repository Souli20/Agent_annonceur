"""
Envoi de notifications par email via SMTP (compatible Gmail avec un
mot de passe d'application : https://myaccount.google.com/apppasswords).
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_TO


def _construire_corps(offres: list[dict]) -> str:
    lignes = [f"{len(offres)} nouvelle(s) opportunité(s) trouvée(s) :\n"]
    for o in offres:
        lignes.append(
            f"- {o['titre']} — {o.get('entreprise', 'N/A')} "
            f"({o.get('lieu', 'N/A')}) [{o.get('source')}]\n  {o.get('lien')}\n"
        )
    return "\n".join(lignes)


def envoyer(offres: list[dict]) -> None:
    if not offres:
        return

    corps = _construire_corps(offres)

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"[Veille opportunités] {len(offres)} nouvelle(s) offre(s)"
    msg.attach(MIMEText(corps, "plain", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, EMAIL_TO, msg.as_string())

    print(f"[email] {len(offres)} offre(s) envoyée(s) à {EMAIL_TO}")
