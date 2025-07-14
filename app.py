import os
from urllib.parse import quote_plus
import feedparser
import smtplib
from email.mime.text import MIMEText

def main():
    # Λέξεις-κλειδιά (με location ενσωματωμένη)
    keywords = [
        'internal auditor Athens',
        'audit assistant Athens',
        'financial controller Athens'
    ]

    # Δημιουργία query
    query = ' OR '.join(keywords)  
    encoded_query = quote_plus(query)  # κωδικοποίηση URL

    # Τελικό RSS URL (χωρίς &l=)
    rss_url = f'https://rss.indeed.com/rss?q={encoded_query}'

    # Φόρτωμα του feed
    feed = feedparser.parse(rss_url)

    # Συλλογή αγγελιών
    jobs = [f"{entry.title}\n{entry.link}" for entry in feed.entries]

    # Σώμα email
    body = "\n\n".join(jobs) if jobs else "Δεν βρέθηκαν νέες αγγελίες σήμερα."

    # Σύνταξη και αποστολή email
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = 'Νέες Θέσεις Εργασίας'
    msg['From']    = os.environ['EMAIL_USER']
    msg['To']      = os.environ['EMAIL_USER']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

if __name__ == "__main__":
    main()

