# Agent de veille d'opportunités

Agent Python qui surveille automatiquement des offres de stages/emplois
(data, statistiques, économie) sur plusieurs sources en ligne, filtre les
offres pertinentes, évite les doublons, et t'envoie une notification par
email et/ou WhatsApp.

## Structure du projet

```
veille-opportunites/
├── main.py                  # point d'entrée : collecte -> filtre -> envoie
├── config.py                # toute la configuration (mots-clés, identifiants)
├── db.py                    # base SQLite locale pour éviter les doublons
├── filtre.py                # logique de filtrage par mots-clés
├── sources/
│   ├── remoteok.py          # source active : API RemoteOK (gratuite)
│   ├── remotive.py          # source active : API Remotive (gratuite)
│   └── _modele_nouvelle_source.py  # modèle pour ajouter une source par scraping
├── notifier/
│   ├── email_sender.py      # envoi par email (SMTP)
│   └── whatsapp_sender.py   # envoi par WhatsApp (Twilio)
├── .github/workflows/veille.yml  # exécution automatique via GitHub Actions
├── requirements.txt
└── .env.example              # modèle de configuration (copier vers .env)
```

## 1. Installation locale (pour tester)

```bash
cd veille-opportunites
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Édite ensuite `.env` avec tes vraies informations (voir section suivante).

## 2. Configurer l'email (Gmail)

1. Active la validation en deux étapes sur ton compte Google
2. Génère un "mot de passe d'application" : https://myaccount.google.com/apppasswords
3. Renseigne `SMTP_USER` (ton adresse Gmail) et `SMTP_PASSWORD`
   (le mot de passe d'application, pas ton mot de passe Gmail normal) dans `.env`
4. Renseigne `EMAIL_TO` avec l'adresse qui doit recevoir les alertes

## 3. Configurer WhatsApp (optionnel, via Twilio)

1. Crée un compte sur https://www.twilio.com/whatsapp
2. Active le "WhatsApp Sandbox" (gratuit pour tester) ou un numéro WhatsApp Business officiel
3. Récupère `Account SID` et `Auth Token` sur le dashboard Twilio
4. Dans `.env`, mets `WHATSAPP_ENABLED=true` et renseigne :
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_FROM` (numéro sandbox Twilio par défaut : `whatsapp:+14155238886`)
   - `WHATSAPP_TO=whatsapp:+2260644961XX` (ton numéro, format international)
5. Si tu utilises le sandbox, envoie d'abord le message `join <code>` fourni par
   Twilio depuis WhatsApp vers leur numéro pour autoriser la réception.

## 4. Lancer manuellement

```bash
python main.py
```

Tu devrais voir dans la console le nombre d'offres collectées, filtrées, et
nouvelles — et recevoir un email/WhatsApp si des offres nouvelles existent.

## 5. Automatiser l'exécution

### Option A — GitHub Actions (recommandé, gratuit, zéro serveur)

1. Crée un dépôt GitHub et pousse ce dossier dedans
2. Dans **Settings > Secrets and variables > Actions**, ajoute les secrets :
   `SMTP_USER`, `SMTP_PASSWORD`, `EMAIL_TO`, et si besoin `WHATSAPP_ENABLED`,
   `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`, `WHATSAPP_TO`
3. Le workflow `.github/workflows/veille.yml` tourne automatiquement toutes
   les 6h (modifiable dans le fichier, ligne `cron: "0 */6 * * *"`)
4. Tu peux aussi le lancer manuellement depuis l'onglet **Actions** du dépôt

### Option B — Cron sur ta propre machine/VM

```bash
crontab -e
# Ajoute cette ligne pour lancer toutes les 6h :
0 */6 * * * cd /chemin/vers/veille-opportunites && /chemin/vers/venv/bin/python main.py >> log.txt 2>&1
```

## 6. Ajouter d'autres sources

Les sources actuelles (RemoteOK, Remotive) couvrent bien le remote/tech
international, mais pas forcément les offres locales (Cameroun, CEMAC,
institutions type BAD/PNUD/INS). Pour en ajouter :

1. Copie `sources/_modele_nouvelle_source.py` vers `sources/<nom>.py`
2. Adapte l'URL et les sélecteurs CSS au site ciblé (inspecte le HTML du site)
3. Ajoute le nom du fichier (sans `.py`) à `ACTIVE_SOURCES` dans `config.py`

Sites à considérer pour un profil ISE/data/éco : Emploi.cm, Jobartis,
LinkedIn Jobs (recherche par mots-clés + RSS via un service tiers), les
pages carrières de la BAD, la Banque Mondiale, le PNUD, la CEMAC, l'INS.

## 7. Ajuster les mots-clés

Modifie `KEYWORDS_INCLUDE` et `KEYWORDS_EXCLUDE` dans `config.py` pour
affiner ce qui te concerne (ex: ajouter "économétrie", "ingénieur
statisticien", retirer "junior" si tu veux aussi voir les postes confirmés).

## Notes

- La base `offres_vues.db` grossit avec le temps ; ce n'est pas un problème
  (quelques Ko par milliers d'offres), mais tu peux la vider pour repartir
  de zéro (tu recevras alors à nouveau toutes les offres actuellement filtrées).
- Respecte toujours les conditions d'utilisation et le `robots.txt` des
  sites que tu scrapes.
