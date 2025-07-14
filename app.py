import os
import feedparser
import smtplib
from email.mime.text import MIMEText

# Λέξεις-κλειδιά και τοποθεσία
keywords = ['internal auditor', 'audit assistant', 'financial controller']
location = 'Αθήνα'

# Indeed RSS Feed URL (σωστός σύνδεσμος RSS)
rss_url = f'https://gr.indeed.com/rss?q={"%20OR%20".join(keywords)}&l={location}'

# Τράβηγμα δεδομένων
feed = feedparser.parse(rss_url)

jobs = []
for entry in feed.entries:
    jobs.append(f"{entry.title}\n{entry.link}")

if jobs:
    body = "\n\n".join(jobs)
else:
    body = "Δεν βρέθηκαν νέες αγγελίες σήμερα."

# Αποστολή email
msg = MIMEText(body)
msg['Subject'] = 'Νέες θέσεις εργασίας'
msg['From'] = os.environ['EMAIL_USER']
msg['To'] = os.environ['EMAIL_USER']

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
    server.send_message(msg)
