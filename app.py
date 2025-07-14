import os
from urllib.parse import quote_plus
import feedparser
import smtplib
from email.mime.text import MIMEText

def main():
    # Ορισμός keywords και τοποθεσίας
    keywords = ['internal auditor', 'audit assistant', 'financial controller']
    location = 'Αθήνα'

    # Κωδικοποίηση παραμέτρων για το URL
    query = ' OR '.join(keywords)
    encoded_query = quote_plus(query)
    encoded_loc = quote_plus(location)

    # Σύνδεσμος RSS Indeed
    rss_url = f'https://gr.indeed.com/rss?q={encoded_query}&l={encoded_loc}'

    # Ανάγνωση του feed
    feed = feedparser.parse(rss_url)

    # Συλλογή αγγελιών
    jobs = []
    for entry in feed.entries:
        jobs.append(f"{entry.title}\n{entry.link}")

    # Δημιουργία σώματος email
    if jobs:
        body = "\n\n".join(jobs)
    else:
        body = "Δεν βρέθηκαν νέες αγγελίες σήμερα."

    # Σύνταξη και αποστολή email
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = 'Νέες Θέσεις Εργασίας'
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = os.environ['EMAIL_USER']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

if __name__ == "__main__":
    main()
