import os
import smtplib
from email.mime.text import MIMEText

def main():
    # Email body content
    msg = MIMEText("Αυτές είναι οι σημερινές αγγελίες εργασίας.")
    msg['Subject'] = 'Job Alerts'
    msg['From'] = os.environ['EMAIL_USER']
    msg['To'] = os.environ['EMAIL_USER']

    # Send email using Gmail SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
        server.send_message(msg)

if __name__ == "__main__":
    main()
