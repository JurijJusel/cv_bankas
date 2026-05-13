import re
import requests
from bs4 import BeautifulSoup
from rich.progress import track
from constants import CATEGORIES


def safe_text(parent, tag, class_=None, default=None):
    """
    Safely extract text from a BeautifulSoup element.
    Returns None if the element is not found.
    Args:        parent: BeautifulSoup element to search within
        tag: HTML tag to find
        class_: (optional) CSS class to match
    return: Text content of the found element or None if not found
    example use: post_upload = safe_text(job_card, "span", "txt_list_2")
    """
    el = parent.find(tag, class_=class_)
    return el.get_text(strip=True) if el else default


def safe_int_from_list(elements, idx=0, default=0):
    """
    Safely extracts an integer from a list of BeautifulSoup elements.
    This function:
    - Takes a list of elements (e.g. result of find_all)
    - Extracts text from element at given index
    - Finds the first number inside the text using regex
    - Converts it to int
    - Returns default if anything fails
        (e.g. index out of range, no number found, conversion error)
    Args:
        elements (Sequence[Any]): List of BeautifulSoup tags or similar objects
        idx (int): Index of the element to extract
        default (int): Value to return if extraction fails
    Returns:
        int: Parsed integer or default value
    Examples:
        strongs = soup.find_all('strong', class_='jobad_stat_value')
        safe_int_from_list(strongs, 0)
        # "511" → 511
        safe_int_from_list(strongs, 1)
        # ">50" → 50
        safe_int_from_list(strongs, 5)
        # IndexError → 0 (default)
        safe_int_from_list([], 0)
        # empty list → 0
    """
    try:
        text = elements[idx].get_text(strip=True)
        match = re.search(r"\d+", text)
        return int(match.group()) if match else default
    except (IndexError, AttributeError, ValueError):
        return default


def safe_attr(parent, tag, attr, class_=None, default=None):
    """
    Safely extracts an attribute (e.g. href, src) from a BeautifulSoup element.
    Args:
        parent: BeautifulSoup object (parent node)
        tag (str): HTML tag name (e.g. "a", "img")
        attr (str): Attribute name to extract (e.g. "href", "src")
        class_ (str | None): Optional CSS class filter
        default: Value to return if element or attribute is missing
    Returns:
        str | None: Attribute value or default if not found
    Examples:
        safe_attr(job_card, "a", "href")
        # "/job/python-dev-123"
        safe_attr(job_card, "img", "src")
        # "https://image.url/logo.jpg"
        safe_attr(job_card, "a", "href", class_="job_link")
        # filtered by class
        safe_attr(job_card, "a", "href")
        # None if missing
    """
    try:
        el = parent.find(tag, class_=class_)
        return el.get(attr) if el and el.get(attr) else default
    except AttributeError:
        return default


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


def filter_new_posts(existing_data: list, new_data: list) -> list:
    """
    Filters out posts that already exist based on post_id.
    """
    existing_ids = {item["post_id"] for item in existing_data}

    return [
        item for item in new_data
        if item["post_id"] not in existing_ids
    ]


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


def build_url_by_category(category):
    """
    Build the URL for scraping job posts based on the given category.
    """
    url_search_category = "https://www.cvbankas.lt"
    return f"{url_search_category}/?keyw=&padalinys%5B%5D={category}&page="


def get_category_url(categ_id):
    """
    Get the URL for scraping job posts based on the given category ID.
    Args:
        categ_id (int): The category ID to get the URL for.
        shoose from CATEGORIES dict in constants.py
    Returns:
        str: The URL corresponding to the given category ID,
        or a message if the category is not found.
    """
    categ_id = int(categ_id)

    if categ_id not in CATEGORIES.values():
        print(f"Category '{categ_id}' not found.")
        return None

    for categ_name, categ_num in CATEGORIES.items():
        if categ_num == categ_id:
            print(f"{categ_id} belongs to: {categ_name}")
            return build_url_by_category(categ_id)
