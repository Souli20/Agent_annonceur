"""
Envoi de notifications par email via SMTP (compatible Gmail avec un
mot de passe d'application : https://myaccount.google.com/apppasswords).

Version enrichie : email HTML mis en forme avec extrait de description,
lieu et date, plus une version texte simple en repli.

Les descriptions renvoyées par certaines sources (RemoteOK, Remotive...)
contiennent du HTML brut (balises <p>, <br>, entités &amp; etc.) : on les
nettoie avant affichage pour éviter d'afficher des caractères/balises
mal formés dans l'email.
"""

import html
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_TO

_BALISE_HTML = re.compile(r"<[^>]+>")
_ESPACES = re.compile(r"\s+")


def _nettoyer_html(texte: str) -> str:
    """Retire les balises HTML et décode les entités (&amp;, &#39;, etc.)."""
    if not texte:
        return ""
    texte = _BALISE_HTML.sub(" ", texte)       # enlève les balises <...>
    texte = html.unescape(texte)                # décode &amp; &#39; &nbsp; etc.
    texte = _ESPACES.sub(" ", texte).strip()    # normalise les espaces/retours à la ligne
    return texte


def _tronquer(texte: str, longueur: int = 300) -> str:
    texte = _nettoyer_html(texte)
    if len(texte) <= longueur:
        return texte
    return texte[:longueur].rsplit(" ", 1)[0] + "…"


def _construire_corps_texte(offres: list[dict]) -> str:
    """Version texte simple (repli si le client mail n'affiche pas le HTML)."""
    lignes = [f"{len(offres)} nouvelle(s) opportunité(s) trouvée(s) :\n"]
    for i, o in enumerate(offres, 1):
        lignes.append(
            f"{i}. {_nettoyer_html(o['titre'])} — {_nettoyer_html(o.get('entreprise', 'N/A'))}\n"
            f"   Lieu : {_nettoyer_html(o.get('lieu', 'N/A'))}  |  Source : {o.get('source', 'N/A')}"
            f"{'  |  Publié : ' + o.get('date') if o.get('date') else ''}\n"
            f"   {_tronquer(o.get('description', ''), 300)}\n"
            f"   Lien : {o.get('lien')}\n"
        )
    return "\n".join(lignes)


def _construire_corps_html(offres: list[dict]) -> str:
    """Version HTML mise en forme, avec extrait de description nettoyé par offre."""
    cartes = []
    for o in offres:
        titre = html.escape(_nettoyer_html(o.get("titre", "")))
        entreprise = html.escape(_nettoyer_html(o.get("entreprise", "N/A")))
        lieu = html.escape(_nettoyer_html(o.get("lieu", "N/A")))
        source = html.escape(o.get("source", "N/A"))
        date = html.escape(o.get("date", "")) if o.get("date") else ""
        description = html.escape(_tronquer(o.get("description", ""), 300))
        lien = o.get("lien", "#")

        cartes.append(f"""
        <div style="border:1px solid #e0e0e0; border-radius:8px; padding:16px; margin-bottom:14px;">
          <div style="font-size:16px; font-weight:bold; color:#1a1a1a; margin-bottom:4px;">
            <a href="{lien}" style="color:#1a56db; text-decoration:none;">{titre}</a>
          </div>
          <div style="font-size:14px; color:#444; margin-bottom:6px;">
            {entreprise} — {lieu}
          </div>
          <div style="font-size:12px; color:#888; margin-bottom:8px;">
            Source : {source}{f" · Publié : {date}" if date else ""}
          </div>
          {f'<div style="font-size:13px; color:#333; line-height:1.4;">{description}</div>' if description else ''}
          <div style="margin-top:10px;">
            <a href="{lien}" style="font-size:13px; color:#1a56db;">Voir l'offre →</a>
          </div>
        </div>
        """)

    return f"""
    <html>
      <body style="font-family: Arial, sans-serif; max-width:640px; margin:0 auto; padding:16px;">
        <h2 style="color:#1a1a1a;">{len(offres)} nouvelle(s) opportunité(s) trouvée(s)</h2>
        {''.join(cartes)}
        <p style="font-size:12px; color:#999; margin-top:20px;">
          Envoyé automatiquement par ton agent de veille d'opportunités.
        </p>
      </body>
    </html>
    """


def envoyer(offres: list[dict]) -> None:
    if not offres:
        return

    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USER
    msg["To"] = EMAIL_TO
    msg["Subject"] = f"[Veille opportunités] {len(offres)} nouvelle(s) offre(s)"

    # Le client mail affiche la version HTML si possible, sinon la version texte.
    msg.attach(MIMEText(_construire_corps_texte(offres), "plain", "utf-8"))
    msg.attach(MIMEText(_construire_corps_html(offres), "html", "utf-8"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, EMAIL_TO, msg.as_string())

    print(f"[email] {len(offres)} offre(s) envoyée(s) à {EMAIL_TO}")
