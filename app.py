import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText

def main():
    # λέξεις-κλειδιά + τοποθεσία
    keywords = ['internal auditor', 'audit assistant', 'financial controller']
    location = 'Athens'

    # χτίζουμε το query string
    query = '+'.join(keywords + [location])
    url = f'https://www.indeed.com/jobs?q={query}&l={location}'

    # αίτημα και parse
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'lxml')

    # βρίσκουμε τις πρώτες 10 αγγελίες
    jobs = []
    cards = soup.select('a.tapItem')[:10]
    for card in cards:
        title = card.select_one('h2.jobTitle').get_text(strip=True)
        link  = 'https://www.indeed.com' + card['href']
        company = card.select_one('.companyName').get_text(strip=True) if card.select_one('.companyName') else ''
        jobs.append(f"{title} @ {company}\n{link}")

    # σώμα email
    if jobs:
        body = "\n\n".join(jobs)
    else:
        body = "Δεν βρέθηκαν νέες αγγελίες σήμερα."

    # σύνταξη + αποστολή email
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = 'Νέες Θέσεις Εργασίας'
    msg['From']    = os.environ['EMAIL_USER']
    msg['To']      = os.environ['EMAIL_USER']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
        s.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        s.send_message(msg)

if __name__ == '__main__':
    main()
