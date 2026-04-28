import re


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
