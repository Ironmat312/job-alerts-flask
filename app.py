import os
import requests
import smtplib
from email.mime.text import MIMEText

# 1) grab your Adzuna credentials & email creds from env
APP_ID     = os.environ['ADZUNA_APP_ID']
APP_KEY    = os.environ['ADZUNA_APP_KEY']
EMAIL_USER = os.environ['EMAIL_USER']
EMAIL_PASS = os.environ['EMAIL_PASS']
TO_ADDRESS = EMAIL_USER  # or any list you like

# 2) build your search
WHAT     = "internal auditor OR audit assistant OR financial controller"
WHERE    = "London"
COUNTRY  = "gb"  # must be one of Adzuna’s supported ISO codes
PAGE     = 1
PER_PAGE = 20

url = (
    f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{PAGE}"
    f"?app_id={APP_ID}&app_key={APP_KEY}"
    f"&what={requests.utils.quote(WHAT)}"
    f"&where={requests.utils.quote(WHERE)}"
    f"&results_per_page={PER_PAGE}"
)

# 3) fetch & parse
resp = requests.get(url)
resp.raise_for_status()
jobs = resp.json().get('results', [])

# 4) format email body
if not jobs:
    body = "No new job listings found today."
else:
    lines = []
    for j in jobs:
        title = j.get('title')
        loc   = j.get('location', {}).get('display_name')
        date  = j.get('created')
        link  = j.get('redirect_url')
        lines.append(f"• {title} @ {loc} ({date})\n  {link}")
    body = "\n\n".join(lines)

msg = MIMEText(body, _charset='utf-8')
msg['Subject'] = "📬 Daily Job Alerts"
msg['From']    = EMAIL_USER
msg['To']      = TO_ADDRESS

# 5) send it
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(EMAIL_USER, EMAIL_PASS)
    server.send_message(msg)
print("Done sending email.")
