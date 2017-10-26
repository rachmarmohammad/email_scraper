# import pika
import json
import requests
import pycurl
from io import BytesIO
from urllib.parse import urlencode
from urllib.parse import urlsplit
from time import time
from time import sleep
from bs4 import BeautifulSoup
import requests
import requests.exceptions
from collections import deque
import re
import sys
import _thread


def scrapeMail(main_domain):
   # print("scraping mail from " + main_domain)
    # a queue of urls to be crawled
    new_urls = deque([main_domain])z

    # a set of urls that we have already crawled
    processed_urls = set()

    # a set of crawled emails
    emails = set()

    # process urls one by one until we exhaust the queue
    while len(new_urls):
        sleep(1)
        url = new_urls.popleft()
        processed_urls.add(url)
        # print(url)
        sys.stdout.flush()
        # extract base url to resolve relative links
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        path = url[:url.rfind('/') + 1] if '/' in parts.path else url

        try:
            response = requests.get(url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            continue

        # extract all email addresses and add them into the resulting set
        new_emails = set(re.findall(
            r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        tmp = []
        for x in new_emails:
            if ".co" in x or ".net" in x:
                tmp.append(x)
            pass
        # if ".png" not in
        emails.update(tmp)

        if len(emails) > 0 or len(processed_urls) > 15:
            sys.stdout.flush()
            if len(list(emails)) > 0:
                return list(emails)[0]
            else:
                return "None"

        # create a beutiful soup for the html document
        soup = BeautifulSoup(response.text, "lxml")

        # find and process all the anchors in the document
        for anchor in soup.find_all("a"):
            # extract link url from the anchor
            link = anchor.attrs["href"] if "href" in anchor.attrs else ''
            # resolve relative links
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            # add the new url to the queue if it was not enqueued nor processed
            # yet
            if not link in new_urls and not link in processed_urls:
                if main_domain in link and ".pdf" not in link and ".png" not in link and ".jpg" not in link and "#" not in link:
                    new_urls.append(link)
    return "None"


print(scrapeMail(sys.argv[1]))
