def safe_text(parent, tag, class_=None):
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
    return el.get_text(strip=True) if el else None

#post_upload = safe_text(job_card, "span", "txt_list_2")
#salary = safe_text(job_card, "span", "salary_amount")
#salary_type = safe_text(job_card, "span", "salary_calculation")

def safe_text(parent, tag, class_=None, default=None):
    try:
        el = parent.find(tag, class_=class_)
        return el.get_text(strip=True) if el else default
    except Exception:
        return default


#import re

#def safe_int(parent, tag, class_=None, default=0):
#    el = parent.find(tag, class_=class_)
#    if not el:
#        return default
#    match = re.search(r"\d+", el.get_text())
#    return int(match.group()) if match else default
