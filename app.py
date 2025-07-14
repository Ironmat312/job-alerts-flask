import os
import requests
import feedparser
import smtplib
from email.message import EmailMessage

# ——————  ΡΥΘΜΙΣΕΙΣ  ——————
ADZUNA_APP_ID  = os.environ['ADZUNA_APP_ID']
ADZUNA_APP_KEY = os.environ['ADZUNA_APP_KEY']
EMAIL_USER     = os.environ['EMAIL_USER']
EMAIL_PASS     = os.environ['EMAIL_PASS']

COUNTRY        = 'gb'       # ένας από: at, au, be, br, ca, ch, de, es, fr, gb, in, it, mx, nl, nz, pl, sg, us, za
WHAT           = 'internal auditor'
WHERE          = 'Athens'
PER_PAGE       = 5

# φτιάχνουμε το URL
rss_url = (
    f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
    f"?app_id={ADZUNA_APP_ID}"
    f"&app_key={ADZUNA_APP_KEY}"
    f"&what={requests.utils.quote(WHAT)}"
    f"&where={requests.utils.quote(WHERE)}"
    f"&results_per_page={PER_PAGE}"
)

# 1) Φορτώνουμε τα αποτελέσματα
resp = requests.get(rss_url)
resp.raise_for_status()
data = resp.json()
jobs = data.get('results', [])

# 2) Αν δεν βρήκαμε νέες αγγελίες, σταματάμε
if not jobs:
    print("DEBUG: Βρήκα 0 αγγελίες")
    exit(0)

# 3) Φτιάχνουμε το σώμα του email
body = "\n\n".join(
    f"{j['title']} at {j['company']['display_name']} ({j['location']['area'][1]})\n{j['redirect_url']}"
    for j in jobs
)

# 4) Στέλνουμε email
msg = EmailMessage()
msg['Subject'] = "🔔 Νέες θέσεις Εργασίας – Αθήνα"
msg['From']    = EMAIL_USER
msg['To']      = EMAIL_USER
msg.set_content(body)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_USER, EMAIL_PASS)
    smtp.send_message(msg)

print(f"DEBUG: Στάλθηκαν {len(jobs)} αγγελίες στο {EMAIL_USER}")
