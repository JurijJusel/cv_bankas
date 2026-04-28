def build_url(category):
    """
    Build the URL for scraping job posts based on the given category.
    """
    url_search_category = "https://www.cvbankas.lt"
    return f"{url_search_category}/?keyw=&padalinys%5B%5D={category}"
