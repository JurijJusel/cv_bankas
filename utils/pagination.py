from rich.progress import track
from utils.http_get_soup import get_soup


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
