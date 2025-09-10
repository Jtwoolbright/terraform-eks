# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import boto3
import os
from datetime import datetime

URL = "https://news.ycombinator.com/"
S3_BUCKET = os.getenv("S3_BUCKET", "my-scraper-bucket")

def scrape():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    titles = [a.get_text() for a in soup.select(".storylink")]
    return {"timestamp": datetime.utcnow().isoformat(), "titles": titles}

def upload_to_s3(data):
    s3 = boto3.client("s3")
    key = f"scrapes/{datetime.utcnow().isoformat()}.json"
    s3.put_object(Bucket=S3_BUCKET, Key=key, Body=json.dumps(data))

if __name__ == "__main__":
    data = scrape()
    upload_to_s3(data)
