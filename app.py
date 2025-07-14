import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import smtplib
from email.mime.text import MIMEText

def main():
    # 1) keywords + τοποθεσία
    keywords = ['internal auditor', 'audit assistant', 'financial controller']
    location = 'Athens'

    # 2) φτιάχνουμε και κωδικοποιούμε το query
    full_query = ' '.join(keywords + [location])
    encoded_query = quote_plus(full_query)

    # 3) URL για Indeed (24ωρης δημοσίευσης)
    url = f'https://www.indeed.com/jobs?q={encoded_query}&fromage=1'

    # 4) κάνουμε request
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'lxml')

    # 5) δοκιμάζουμε διαφορετικό selector: div.job_seen_beacon
    cards = soup.select('div.job_seen_beacon')[:10]
    print(f"DEBUG: Βρήκα {len(cards)} αγγελίες")  # θα φανεί στα logs

    jobs = []
    for card in cards:
        # τίτλος
        title_tag = card.select_one('h2.jobTitle > span')
        title = title_tag.get_text(strip=True) if title_tag else '—'

        # εταιρεία
        comp_tag = card.select_one('span.companyName')
        company = comp_tag.get_text(strip=True) if comp_tag else ''

        # link
        link_tag = card.find('a', href=True)
        href = link_tag['href'] if link_tag else ''
        link = ('https://www.indeed.com' + href) if href.startswith('/') else href

        jobs.append(f"{title} @ {company}\n{link}")

    # 6) σώμα email
    body = "\n\n".join(jobs) if jobs else "Δεν βρέθηκαν νέες αγγελίες σήμερα."

    # 7) στέλνουμε email
    msg = MIMEText(body, _charset='utf-8')
    msg['Subject'] = 'Νέες Θέσεις Εργασίας'
    msg['From']    = os.environ['EMAIL_USER']
    msg['To']      = os.environ['EMAIL_USER']

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

if __name__ == '__main__':
    main()
