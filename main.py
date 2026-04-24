from crawlers.cv_bank_scraper import scrape_all_posts
from constants import PYTHON_URL, BASE_URL
from rich import print


if __name__ == "__main__":
    scrape_all_posts(BASE_URL)
    print("DONE!!!")
