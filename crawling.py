import requests
from bs4 import BeautifulSoup


def crawling_book(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, "html.parser")

    title = soup.select_one('meta[property="og:title"]')["content"]
    title = title.split(":")[0].strip()
    desc = soup.select_one(
        "#container > div.bookCatalog_inner_container__JUfKQ > div.bookCatalog_book_catalog__yiiIc > div.bookCatalog_book_info_top__SUILS > div.bookSummary_book_summary__NsCmt > div.bookIntro_book_intro__BzWNC > div"
    ).text
    desc = " ".join(desc.split())
    image = soup.select_one('meta[property="og:image"]')["content"]
    author = soup.select_one(
        "#container > div.bookCatalog_inner_container__JUfKQ > div.bookCatalog_book_catalog__yiiIc > div.bookCatalog_book_info_top__SUILS > div.bookSummary_book_summary__NsCmt > div.bookTitle_book_title__e3mof > div.bookTitle_detail_area__0yrpT > ul.bookTitle_list_info__yXUyF > li:nth-child(1) > div.bookTitle_info_content__iHfCC > span"
    ).text
    crawling_book = {
        "title": title,
        "author": author,
        "desc": desc,
        "image": image,
    }
    return crawling_book
