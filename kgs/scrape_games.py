from collections import namedtuple
from datetime import datetime, timedelta
import os
import time
from urlparse import parse_qs, urlparse

from bs4 import BeautifulSoup
import requests

from django.core.files.base import ContentFile

KgsGame = namedtuple("KgsGame", "sgf_url white black date type result")

def rate_limited(secs):
    def deco(f):
        def wrapped(*args, **kwargs):
            time.sleep(secs)
            return f(*args, **kwargs)
        return wrapped
    return deco


KGS_url = "http://www.gokgs.com/gameArchives.jsp"
KGS_timestamp_format = "%m/%d/%y %I:%M %p"

@rate_limited(5)
def get_raw_KGS_data(username, year, month):
    qparams = {
        "user": username,
        "year": str(year),
        "month": str(month),
    }
    response = requests.get(KGS_url, params=qparams)
    if response.status_code >= 300:
        raise Exception("KGS call failed: %s" % response.text)
    return response.text

def username_from_url(url):
    parsed_url = urlparse(url)
    queryparams = parse_qs(parsed_url.query)
    return queryparams.get("user", [""])[0]

def process_KGS_game_row(row):
    columns = row.find_all("td")
    if len(columns) == 7:
        sgf_url = columns[0].a['href']
        white = username_from_url(columns[1].a['href']).lower()
        black = username_from_url(columns[2].a['href']).lower()
        date = datetime.strptime(columns[4].text, KGS_timestamp_format).date()
        type_ = columns[5].text
        result = columns[6].text
        return KgsGame(sgf_url, white, black, date, type_, result)
    elif len(columns) == 6:
        sgf_url = columns[0].a['href']
        white = username_from_url(columns[1].a['href']).lower()
        black = ""
        date = datetime.strptime(columns[3].text, KGS_timestamp_format).date()
        type_ = columns[4].text
        result = columns[5].text
        return KgsGame(sgf_url, white, black, date, type_, result)
    else:
        return KgsGame("", "", "", "", "", "")

def process_KGS_page(rawtext):
    soup = BeautifulSoup(rawtext)
    try:
        rows = soup.find_all("table")[0].find_all("tr")[1:]
        return map(process_KGS_game_row, rows)
    except IndexError:
        return []

def get_KGS_games(username, year, month):
    return process_KGS_page(get_raw_KGS_data(username, year, month))

def get_filename(url):
    parsed_url = urlparse(url)
    return os.path.split(parsed_url.path)[1]

def download_gamefile(url):
    response = requests.get(url)
    return ContentFile(response.content, name=get_filename(url))

def filter_likely_games(KGS_name1, KGS_name2, date=None):
    KGS_name1 = KGS_name1.lower()
    KGS_name2 = KGS_name2.lower()
    def filterer(kgs_game):
        if kgs_game.type == "Review" or kgs_game.result == "Unfinished":
            return False
        if date is not None:
            if abs(date - kgs_game.date) > timedelta(days=7):
                return False
        return ((kgs_game.black.startswith(KGS_name1) and kgs_game.white.startswith(KGS_name2)) or
                (kgs_game.black.startswith(KGS_name2) and kgs_game.white.startswith(KGS_name1)))
    return filterer
