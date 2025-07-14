import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import smtplib
from email.mime.text import MIMEText

def main():
    # λέξεις-κλειδιά και τοποθεσία
    keywords = ['internal auditor', 'audit assistant', 'financial controller']
    location = 'Athens'

    # χτίζουμε query + το κωδικοποιούμε
    full_query = ' '.join(keywords + [location])
    encoded_query = quote_plus(full_query)

    # URL αναζήτησης (παίρνει τις πιο πρόσφατες)
    # Επιπλέον μπορούμε να προσθέσουμε &fromage=1 για θέσεις 24ωρου:
    url = f'https://www.indeed.com/jobs?q={encoded_query}&fromage=1'

    # αίτημα και parse
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'lxml')

    # βρίσκουμε τις πρώτες 10 αγγελίες
    cards = soup.select('a.tapItem')[:10]
    jobs = []
    for card in cards:
        title = card.select_one('h2.jobTitle').get_text(strip=True)
        link  = 'https://www.indeed.com' + card['href']
        company = card.select_one('.companyName').get_text(strip=True) if card.select_one('.companyName') else ''
        jobs.append(f"{title} @ {company}\n{link}")

    # σώμα email
    body = "\n\n".join(jobs) if jobs else "Δεν βρέθηκαν νέες αγγελίες σήμερα."

    # σύνταξη + αποστολή email
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = 'Νέες Θέσεις Εργασίας'
    msg['From']    = os.environ['EMAIL_USER']
    msg['To']      = os.environ['EMAIL_USER']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

if __name__ == '__main__':
    main()
