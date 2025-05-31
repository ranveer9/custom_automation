# Custom Scraper
import os
import smtplib
import requests
from dotenv import load_dotenv
from datetime import datetime
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

#  Environment Variables
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
APP_PASSWORD = os.getenv("APP_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

def get_top_local_news():
    """
    Scrapes the data along with links from the local news website.
    """
    url = "https://www.tribuneindia.com/news/city/chandigarh"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for h2_tag in soup.find_all("h2"):
        link = h2_tag.find("a")
        if link:
            title = link.get_text(strip=True)
            href = link.get("href")

            if title and href and href != "#":

                full_url = f"https://www.tribuneindia.com{href}" if href.startswith("/") else href

                articles.append((title, full_url))

                if len(articles)>=10:
                    break
                
    return articles

def send_email(headlines):
    """
    Sends an email to the user.
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Your Daily Top 10 Chandigarh News - {datetime.now().strftime("%d/%m/%Y")}"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    html_content = "<h2>Top 5 Chandigarh News Headlines</h2><ol>"
    for title, link in headlines:
        html_content += f"<li><a href='{link}'>{title}</a></li>\n"
    html_content+="</ol>"

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, APP_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
    
    print("Email sent successfully!")

def job():
    headlines = get_top_local_news()
    send_email(headlines)

job()