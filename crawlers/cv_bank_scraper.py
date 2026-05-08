from rich.progress import track
from constants import BASE_URL, PYTHON_URL
from models.post_model import JobPostModel
from utils.scraper_helpers import safe_int_from_list, safe_text, safe_attr
from utils.http_get_soup import get_soup
from utils.pagination import get_total_count_pages


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
    """
    Scrapes all job posts from the given URL and returns a list of job post data.
    Args:
        url (str): The base URL to scrape job posts from.
    Returns:
        all_posts (list): A list of dictionaries containing job post data.
    """
    soup = get_soup(url)
    count_pages = get_total_count_pages(soup)
    print(f"Total pages: {count_pages}")

    all_posts = []

    for page in track(range(count_pages), description="Processing..."):
        page_url = f"{url}{page+1}"
        page_soup = get_soup(page_url)
        print(f"Scraping page: {page_url}")

        articles = page_soup.find_all("article")

        for article in track(articles, description="Processing job posts ..."):
            try:
                job_card = scrape_post(article)
            except Exception as e:
                print(f"Failed post: {e}")

            post_obj_model = JobPostModel(**job_card)
            post_json = post_obj_model.model_dump(mode="json")
            all_posts.append(post_json)

    return all_posts
