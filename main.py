from crawlers.cv_bank_scraper import scrape_all_posts
from constants import PYTHON_URL
from rich import print
from utils.file import write_data_to_json_file
from utils.scraper_helpers import get_category_url
from constants import CV_BANKAS_JSON_FILE_PATH


def main():
    url = get_category_url(81) or PYTHON_URL
    scrape_posts= scrape_all_posts(url)
    print(write_data_to_json_file(scrape_posts, CV_BANKAS_JSON_FILE_PATH))


if __name__ == "__main__":
    main()
    print("DONE!!!")
