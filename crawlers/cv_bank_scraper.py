from bs4 import BeautifulSoup
import requests
from rich.progress import track
from constants import BASE_URL, PYTHON_URL
from models.post_model import JobPostModel
from utils.scraper_helpers import safe_int_from_list, safe_text, safe_attr


def get_soup(url: str) -> BeautifulSoup | None:
    """
    Fetches and parses a webpage into a BeautifulSoup object.
    Args:
        page_url (str): The full URL of the page to fetch.
    Returns:
        BeautifulSoup: Parsed HTML content of the page.
    """
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        return soup

    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def get_all_count_of_posts(count_pages, base_url):
    """
    Extracts the total count of posts from the webpage.
    Args:
        count_pages (int): The number of pages to iterate through.
        base_url (str): The base URL for the pages.
    Returns:
        int: Total count of posts.
    """
    total_posts = 0
    for page in track(range(count_pages), description="Processing..."):
        url = f"{base_url}{page+1}"
        print(url)
        soup = get_soup(url)
        articles = soup.find_all("article")
        articles_search = int(len(articles))
        total_posts += articles_search
    return total_posts


def get_total_count_pages(soup):
    """
    Extracts the total number of pages from the pagination section of the webpage.
    Args:
        soup (BeautifulSoup): Parsed HTML content of the page.
    Returns:
        int: The total number of pages.
    """
    pages_ul = soup.find("ul", class_="pages_ul_inner")
    pages_li = pages_ul.find_all("li")[-1:]
    last_page_number = pages_li[0].find("a").get_text()
    return int(last_page_number)


def scrape_post(job_card_article):
    post_id = job_card_article.find("div", class_= "jobadlist_ad_anchor").get("id")[6:]
    post_url = safe_attr(job_card_article, "a", "href", class_="list_a can_visited list_a_has_logo")
    company_logo_url = safe_attr(job_card_article, "img", "src")
    position = job_card_article.find("h3").text
    company = job_card_article.find("span", class_="heading_secondary").get_text().strip()
    salary = safe_text(job_card_article, "span", "salary_amount")
    salary_type = safe_text(job_card_article, "span", "salary_calculation")
    post_upload = safe_text(job_card_article, "span", "txt_list_2")

    post_url_soup = get_soup(post_url)
    company_city = post_url_soup.find('span', {'itemprop': 'addressLocality'}).get_text().strip()
    strong_selector = post_url_soup.find_all('strong', class_='jobad_stat_value')
    people_viewed = safe_int_from_list(strong_selector, 0)
    people_applied = safe_int_from_list(strong_selector, 1)

    data =  {
        "post_id": post_id,
        "company": company,
        "company_city": company_city,
        "position": position,
        "salary": salary,
        "salary_type": salary_type,
        "post_url": post_url,
        "company_logo_url": company_logo_url,
        "post_upload": post_upload,
        "people_viewed": people_viewed,
        "people_applied": people_applied
    }

    return data


def scrape_all_posts(url):
    soup = get_soup(url)
    count_pages = get_total_count_pages(soup)
    print(f"Total pages: {count_pages}")

    for page in track(range(count_pages), description="Processing..."):
        page_url = f"{url}{page+1}"
        page_soup = get_soup(page_url)
        print(f"Scraping page: {page_url}")

        articles = page_soup.find_all("article")

        for article in articles:
            try:
                job_card = scrape_post(article)
            except Exception as e:
                print(f"Failed post: {e}")

            post_obj_model = JobPostModel(**job_card)

            print("= "*20)
            print(post_obj_model)


if __name__ == "__main__":
    #soup = get_soup(BASE_URL)
    #soup = get_soup(PYTHON_URL)
    #total_pages = get_total_count_pages(soup)
    #print(f"Total pages: {total_pages}")
    #total_posts = get_all_count_of_posts(total_pages, PYTHON_URL)
    #print(f"Total posts: {total_posts}")

    #scrape_post(PYTHON_URL)
    print(scrape_all_posts(PYTHON_URL))
    print("DONE!!!")
