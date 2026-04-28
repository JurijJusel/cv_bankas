from crawlers.cv_bank_scraper import scrape_all_posts
from constants import PYTHON_URL
from rich import print
from utils.file import write_data_to_json_file
from constants import CV_BANKAS_JSON_FILE_PATH


if __name__ == "__main__":
    all_posts = scrape_all_posts(PYTHON_URL)
    print(write_data_to_json_file(all_posts, CV_BANKAS_JSON_FILE_PATH))
    print("DONE!!!")
