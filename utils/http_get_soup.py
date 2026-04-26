import requests
from bs4 import BeautifulSoup


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
