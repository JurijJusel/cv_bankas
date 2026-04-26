from crawlers.cv_bank_scraper import scrape_all_posts
from constants import PYTHON_URL
from rich import print


if __name__ == "__main__":
    scrape_all_posts(PYTHON_URL)
    print("DONE!!!")
